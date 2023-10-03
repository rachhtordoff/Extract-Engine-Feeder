import json

from src.dependencies import identity_check_api, doc_api, notifications


class NewDocSqs(object):
    def __init__(self, body):
        print(body)
        report_id=body["report_id"]

        # get document
        document = identity_check_api.get_report(report_id)

        if not document:
            print("an errror occured trying to get the document from identity_check_api")
            return
            # need to add some error handling here to alert us something has happended


        bucket_id = doc_api.get_bucket_staff(client_id)

        # get document type id
        document_type_id = doc_api.get_document_type(company_id, "uploaded_to_staff")

        if not document_type:
            print("an errror occured trying to get the document type id from doc_api for staff")
            return
        # need to add some error handling here to alert us something has happended

        uploaded_doc_details = doc_api.upload_document(bucket_id, document, "{}_{}.pdf".format(insurance_id, document_type), document_type_id)
        if not len(uploaded_doc_details) == 1:
            print("an errror occured trying to upload document to doc_api for staff")
            return
        # need to add some error handling here to alert us something has happended

        uploaded_doc_details = uploaded_doc_details[0]
        document_name = uploaded_doc_details["document_name"]
        document_id = uploaded_doc_details["id"]



        #http://127.0.0.1:6056/insurance/1/documents/PolicySummary
        #id = body["id"]
        #return_queue =  body["return_queue"]

        #solicitorDocCreationCaller = SolicitorDocCreationApi()
        #sqsSender = SqsSender(return_queue)

        #created_doc = solicitorDocCreationCaller.create_doc(id, body)

        #if created_doc:
        #    sqsSender.send_message(created_doc)
        #else:
        #    raise Exception('something has gone wrong calling solicitor document creation api')
