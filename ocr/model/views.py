# check_processor/views.py

from django.shortcuts import render, redirect
from django.views import View
from .forms import CheckUploadForm
from .models import CheckData
from .syndicate_bank import syndicate_extract, extract_ifsc as syndicate_extract_ifsc, extract_account_no as syndicate_extract_account_no, micr_account_no as syndicate_micr_account_no,hand_name,amount_in_numbers,amount
from .axis_bank import extract_ifsc_ax as axis_extract_ifsc, extract_account_no_ax as axis_extract_account_no, micr_account_no as axis_micr_account_no,amount_in_numbers_a
from .icici_bank import extract_ifsc_ic as icici_extract_ifsc, extract_account_no_ic as icici_extract_account_no, micr_account_no as icici_micr_account_no,amount_ic,hand_name_ic,amount_in_numbers_ic
from .canara_bank import extract_ifsc_ca as canara_extract_ifsc, extract_account_no_ca as canara_extract_account_no, micr_account_no as canara_micr_account_no,amount_ca,hand_name_ca,amount_in_numbers_ca
from .general_bank import extract_account_no_gb,extract_ifsc_gb,micr_account_no,amount_gb,amount_in_numbers_gb,hand_name_gb
import os
from .signature_detection import detect_signature 
class CheckUploadView(View):
    def get(self, request):
        form = CheckUploadForm()
        return render(request, 'check_upload.html', {'form': form})

    def post(self, request):
        form = CheckUploadForm(request.POST, request.FILES)
        if form.is_valid() :
            check_data = form.save()
            image_path = check_data.check_image.path

            if check_data.bank_name == 'syndicate':
                rois = syndicate_extract(image_path)
                check_data.name=hand_name(image_path)
                check_data.amount=amount(image_path)
                check_data.amount_in_dg=amount_in_numbers(image_path)
                for roi in rois:
                    ifsc_code = syndicate_extract_ifsc(roi)
                    account_number = syndicate_extract_account_no(roi)
                    if ifsc_code:
                        check_data.ifsc_code = ifsc_code
                    if account_number:
                        check_data.account_number = account_number
                micr_details = syndicate_micr_account_no(image_path)
                if micr_details:
                    check_data.micr_details = micr_details

            elif check_data.bank_name == 'axis':
                ifsc_code = axis_extract_ifsc(image_path)
                check_data.name=hand_name(image_path)
                check_data.amount=amount(image_path)
                check_data.amount_in_dg=amount_in_numbers_a(image_path)
                account_number = axis_extract_account_no(image_path)
                micr_details = axis_micr_account_no(image_path)
                if ifsc_code:
                    check_data.ifsc_code = ifsc_code
                if account_number:
                    check_data.account_number = account_number
                if micr_details:
                    check_data.micr_details = micr_details

            elif check_data.bank_name == 'icici':
                check_data.name=hand_name_ic(image_path)
                check_data.amount=amount_ic(image_path)
                check_data.amount_in_dg=amount_in_numbers_ic(image_path)
                ifsc_code = icici_extract_ifsc(image_path)
                account_number = icici_extract_account_no(image_path)
                micr_details = icici_micr_account_no(image_path)
                if ifsc_code:
                    check_data.ifsc_code = ifsc_code
                if account_number:
                    check_data.account_number = account_number
                if micr_details:
                    check_data.micr_details = micr_details

            elif check_data.bank_name == 'canara':
                check_data.name=hand_name_ca(image_path)
                check_data.amount=amount_ca(image_path)
                check_data.amount_in_dg=amount_in_numbers_ca(image_path)
                ifsc_code = canara_extract_ifsc(image_path)
                account_number = canara_extract_account_no(image_path)
                micr_details = canara_micr_account_no(image_path)
                if ifsc_code:
                    check_data.ifsc_code = ifsc_code
                if account_number:
                    check_data.account_number = account_number
                if micr_details:
                    check_data.micr_details = micr_details
            elif check_data.bank_name == 'general':
                check_data.name=hand_name_gb(image_path)
                check_data.amount=amount_gb(image_path)
                check_data.amount_in_dg=amount_in_numbers_gb(image_path)
                ifsc_code = extract_ifsc_gb(image_path)
                account_number = extract_account_no_gb(image_path)
                micr_details = micr_account_no(image_path)
                if ifsc_code:
                    check_data.ifsc_code = ifsc_code
                if account_number:
                    check_data.account_number = account_number
                if micr_details:
                    check_data.micr_details = micr_details
                    
            check_data.signature_present = detect_signature(image_path)
            check_data.save()
        
            return redirect('check_result', pk=check_data.pk)
        
        return render(request, 'check_upload.html', {'form': form})

class CheckResultView(View):
    def get(self, request, pk):
        check_data = CheckData.objects.get(pk=pk)
        context = {
            'check_data': check_data,
        }
        return render(request, 'check_result.html', context)
