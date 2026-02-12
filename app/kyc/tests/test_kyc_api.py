from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from kyc.models import KYCApplication

User= get_user_model()
class KYCApplicationTests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(email="user@test.com",password="user123",  )

        self.admin = User.objects.create_superuser(email="admin@test.com",password="admin123")
    
    def test_create_application(self):
        self.client.force_authenticate(user=self.user)
        
        #sending empty json body as required to create application
        response=self.client.post("/api/kyc/applications/",{})

        self.assertEqual(response.status_code,201)
        self.assertEqual(KYCApplication.objects.first().user,self.user)

    def test_admin_change_status(self):
        application=KYCApplication.objects.create(user=self.user,current_status="SUBMITTED")    

        self.client.force_authenticate(user=self.admin)

        response=self.client.post(f"/api/kyc/applications/{application.id}/change-status/",{"new_status" :"IN_REVIEW"})
        self.assertEqual(response.status_code,200)
        application.refresh_from_db()
        self.assertEqual(application.current_status,"IN_REVIEW")

    def test_user_cannot_change_status(self):
        application=KYCApplication.objects.create(user=self.user,current_status="SUBMITTED") 
        self.client.force_authenticate(user=self.user)
        response=self.client.post(f"/api/kyc/applications/{application.id}/change-status/",{"new_status" :"IN_REVIEW"})
        self.assertEqual(response.status_code,403)
        application.refresh_from_db()
        self.assertEqual(application.current_status,"SUBMITTED")   

    def test_user_can_resubmit_rejected_application(self):
        application = KYCApplication.objects.create(user=self.user,current_status="REJECTED")
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f"/api/kyc/applications/{application.id}/resubmit/",format="json")

        self.assertEqual(response.status_code, 200)

        application.refresh_from_db()
        self.assertEqual(application.current_status, "SUBMITTED")
    
    def test_user_cannot_resubmit_if_not_rejected(self):
        application = KYCApplication.objects.create(user=self.user,current_status="SUBMITTED")

        self.client.force_authenticate(user=self.user)

        response = self.client.post(f"/api/kyc/applications/{application.id}/resubmit/",format="json")
        self.assertEqual(response.status_code, 400)

        application.refresh_from_db()
        self.assertEqual(application.current_status, "SUBMITTED")

    def test_admin_pending_applications(self):
        KYCApplication.objects.create(user=self.user,current_status="SUBMITTED")
        KYCApplication.objects.create(user=self.user,current_status="IN_REVIEW")
        KYCApplication.objects.create(user=self.user,current_status="REJECTED")

        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/kyc/applications/pending/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  

    def test_user_cannot_view_pending_applications(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/kyc/applications/pending/")

        self.assertEqual(response.status_code, 403)

    def test_invalid_status_transition(self):
         application = KYCApplication.objects.create(user=self.user,current_status="SUBMITTED")
 
         self.client.force_authenticate(user=self.admin)

         response = self.client.post(f"/api/kyc/applications/{application.id}/change-status/",{"new_status": "APPROVED"},format="json" )

         self.assertEqual(response.status_code, 400)

         application.refresh_from_db()
         self.assertEqual(application.current_status, "SUBMITTED")
     
    def test_admin_can_add_review_comment(self):
        application = KYCApplication.objects.create(user=self.user,current_status="IN_REVIEW")

        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
        f"/api/kyc/applications/{application.id}/add-reviewcomment/",{"comment_text": "Looks good."})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(application.comments.count(), 1)

    def test_status_history_created(self):
        application = KYCApplication.objects.create(user=self.user,current_status="IN_REVIEW")
        self.client.force_authenticate(user=self.admin)
        response=self.client.post(f"/api/kyc/applications/{application.id}/change-status/",{"new_status" :"APPROVED"})
        application.refresh_from_db()
        self.assertEqual(application.statushistory.count(),1)
        history=application.statushistory.first()
        self.assertEqual(history.old_status,"IN_REVIEW"),
        self.assertEqual(history.new_status,"APPROVED")


    def test_status_history_list(self):
        application = KYCApplication.objects.create(user=self.user,current_status="SUBMITTED")
        self.client.force_authenticate(user=self.admin)
        application.statushistory.create(old_status="SUBMITTED", new_status="IN_REVIEW",changed_by=self.admin)
        response=self.client.get(f"/api/kyc/applications/{application.id}/history/")

        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),1)
        


    def test_review_comments_list(self):
     application = KYCApplication.objects.create(user=self.user,current_status="IN_REVIEW" )
     application.comments.create(reviewer=self.admin,comment_text="Needs additional document.")
     self.client.force_authenticate(user=self.admin)
     response = self.client.get(f"/api/kyc/applications/{application.id}/reviewcomments/")
     self.assertEqual(response.status_code, 200)
     self.assertEqual(len(response.data), 1)
     self.assertEqual(response.data[0]["comment_text"], "Needs additional document.")



    def test_user_can_upload_document(self):
        application = KYCApplication.objects.create(user=self.user,current_status="SUBMITTED")

        self.client.force_authenticate(user=self.user)

        file = SimpleUploadedFile("test.png",b"dummy content",content_type="image/png")

        response = self.client.post(
        f"/api/kyc/applications/{application.id}/upload-document/",
        {
            "document_type": "ID_PROOF",
            "file": file
        },
        format="multipart"
    )
        self.assertEqual(response.status_code, 201)
        application.refresh_from_db()
        self.assertEqual(application.documents.count(), 1)

    def test_user_can_list_uploaded_documents(self):
        application = KYCApplication.objects.create(user=self.user,current_status="SUBMITTED")

        application.documents.create(document_type="ID_PROOF",file=SimpleUploadedFile("test.png",b"dummy content",content_type="image/png") )

        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/api/kyc/applications/{application.id}/documents/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["document_type"], "ID_PROOF")
