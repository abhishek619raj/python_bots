from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .models import File
from django.http import HttpResponse
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import io
from django.http import HttpResponse
import spacy
nlp = spacy.load("en_core_web_sm")

def pdf_to_text(path):
    with open(path, 'rb') as fp:
        rsrcmgr = PDFResourceManager()
        outfp = io.StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
        text = outfp.getvalue()
        doc = nlp(text)
        case_list = []
        for entity in doc.ents:
            case = {'Text': entity.text, 'Label':  entity.label_ }
            case_list.append(case)
            print(entity.text,entity.label_)
        result = {"pdf_to_text":text.replace('\n',''),
                  "text_label":case_list
                  }
        return Response(result)


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,file_id=None):
        try:
            if(file_id):
                user_data = File.objects.filter(pk=file_id,is_deleted = False)[0]
                get_data = FileSerializer(user_data)
                return pdf_to_text("/home/abhishek/python_bot_work/python_bot"+ get_data.data['file'])
            else:
                user_data = File.objects.filter(is_deleted = False)
                get_data = FileSerializer(user_data,many=True)
            return Response(get_data.data,status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response("Error")
