
import os
from django.conf import settings
from zeep import Client, Settings

def sap_upload_doc(file=None, serial_no=None):
    print(f"--- SAP 'UPLOAD' Integration (File: {file}) ---")
    
    wsdl_path = os.path.join(settings.BASE_DIR, 'standard_app', 'wsdl', 'z_qm_upl_vtr_doc_frm_test_macbinding.wsdl')
    
    if not os.path.exists(wsdl_path):
        print(f"❌ SAP configuration error: WSDL file not found at {wsdl_path}")
        return

    try:
        # Initialize Client
        # Note: XML huge tree enabled for large SOAP responses
        soap_settings = Settings(strict=False, xml_huge_tree=True)
        client = Client(wsdl=wsdl_path, settings=soap_settings)
        print(f"[OK] WSDL Loaded: {os.path.basename(wsdl_path)}")

        if not file or not serial_no:
            print("❌ File name or Serial Number is required for SAP upload")
            return

        # Data for UPLOAD request
        # The SAP service expects IpFilePath in a specific format
        upload_data = {
            'IpFilePath': f'//LTVLCD29338/Reports/{file}',
            'IpUsn': serial_no
        }

        print(f"Attempting to UPLOAD Report: {file}")
        print(f"SAP Path: {upload_data['IpFilePath']}")
        
        # Calling the service
        # Note: We use IpFilePath as the primary identifier for SAP to fetch/store the file
        response = client.service.ZQmUplVtrDocFrmTestMac(**upload_data)
        
        print(f"--- RAW SAP RESPONSE ---")
        print(response)

        # Success/Error logic based on SAP response fields
        success_code = getattr(response, 'EpSuccess', '1')
        exc_msg = getattr(response, 'EpExcmsg', '')

        if success_code == '0':
            print(f"✅ SUCCESS: {file} has been uploaded to SAP.")
        elif "CMS 057" in str(exc_msg):
             print(f"❌ SAP SERVER ERROR (CMS 057) for {file}:")
             print("The SAP Server is trying to start 'sapftp' to reach your PC but it is being blocked.")
             print("FIX: You MUST move the file to a folder the SAP server can see directly (AL11 path).")
        else:
            reason = exc_msg if exc_msg else "Unknown SAP Error (Status 1)"
            print(f"❌ FAILED to upload {file}: {reason}")

    except Exception as e:
        print(f"❌ SAP Connection failed for {file}: {str(e)}")


def get_sap_data(serial_no):
    """
    Fetch valve and test data from SAP using the provided serial number.
    Returns JSON response for AJAX integration in valves.html.
    """
    if  not serial_no:
        return {'status': 'error', 'message': 'Serial number is required.'}

    # Construct WSDL path - located in landtapp/wsdl folder
    wsdl_path = os.path.join(settings.BASE_DIR, 'standard_app', 'wsdl', 'z_qm_get_pres_test_masterbinding.wsdl')
    
    if not os.path.exists(wsdl_path):
        return {'status': 'error', 'message': f'SAP configuration error: WSDL file not found.'}

    is_sap = False

    try:
        if is_sap is False:
            valve_data = {
            "type":"demo data",
            "serial_no": "26C105982",
            "material": "GA14101GM08ASS_004",
            "description": "Gate",
            "size": "14\"",
            "class": "150",
            "sales_order": "0110035345",
            "sales_item": "000120",
            "tag_no": "2002235237; VGGJ10XB 14.000",
            "body_material": "ASTM A216 Gr.WCB",
            "cat_no": "117"
                    }

            trace_details = {
                "BODY": {
                    "heat_no": "AC1002",
                    "mpi_no": "MTA26640",
                    "xray_no": None,
                    "dpi_no": None
                },
                "BONNET": {
                    "heat_no": "AC1002",
                    "mpi_no": "MTA26642",
                    "xray_no": None,
                    "dpi_no": None
                }
            }

            tests = [
                {
                    "testId" : 1,
                    "name": "Seat ( Hydro )",
                    "duration": "120",
                    "pressure_bar": "22.0",
                    "pressure_psi": "315.0",
                    "unit": "SEC"
                },
                {
                    "testId" : 2,
                    "name": "Backseat ( Hydro )",
                    "duration": "120",
                    "pressure_bar": "22.0",
                    "pressure_psi": "315.0",
                    "unit": "SEC"
                },
                {   
                    "testId" : 3,
                    "name": "Seat ( Air )",
                    "duration": "120",
                    "pressure_bar": "7.0",
                    "pressure_psi": "100.0",
                    "unit": "SEC"
                },
                {
                    "testId" : 4,
                    "name": "Shell ( Hydro )",
                    "duration": "300",
                    "pressure_bar": "30.0",
                    "pressure_psi": "450.0",
                    "unit": "SEC"
                }
            ]

            return {
                'status': 'success',
                'valve_details': valve_data,
                'trace_details': trace_details,
                'tests': tests
            }

        # Initialize Zeep Client
        zeep_settings = Settings(strict=False, xml_huge_tree=True)
        client = Client(wsdl=wsdl_path, settings=zeep_settings)

        # Prepare SAP request data
        search_data = {
            'IpMasterDataAll': 'X',
            'IpMbarcodeNum': serial_no,
            'IpProductCode': '1',
            'IpUsn': '',
            'EtPreTestDurVal': {},
            'EtPreTestDuratM': {},
            'EtPreTestValueM': {},
            'EtScndet': {},
            'EtValveAttrMast': {},
        }

        # Call SAP service
        response = client.service.ZQmGetPresTestMaster(**search_data)

        print("responce >>>",response)
        
        # Validation logic from sap_get_demo.py
        is_success = (response.EpSuccess != '1')

        if is_success:
            # Extract basic details
            details = response.EsValveDetail
            valve_data = {
                'serial_no': details.ZfgSlno,
                'material': details.Matnr,
                'description': details.ZprodDesc,
                'size': details.ZprodSize,
                'size_name': details.ZprodSizeDesc,
                'class': details.ZprodClasRatDesc,
                'sales_order': details.Kdauf,
                'sales_item': details.Kdpos,
                'tag_no': details.Tagnum,
                'body_material': details.ZprodMaterialDesc,
                'cat_no': details.ZprodCatgDesc,
            }

            # Extract trace details (Heat No, MPI No)
            trace_details = {}
            if response.EtScndet and response.EtScndet.item:
                for item in response.EtScndet.item:
                    desc = (item.ZtrDesc or '').upper()
                    trace_details[desc] = {
                       
                        'heat_no': item.ZheatNo,
                        'mpi_no': item.ZmpiNo,
                        'xray_no': item.ZxrayNo,
                        'dpi_no': item.ZdpiNo
                    }

            # Extract test specifications
            tests = []
            if response.EtPreTestDurVal and response.EtPreTestDurVal.item:
                for item in response.EtPreTestDurVal.item:
                    tests.append({
                        'testId' : item.ZprTestType,
                        'name': item.ZprTestTypTxt,
                        'duration': item.ZtestDuration,
                        'pressure_bar': item.ZtestPrValBar,
                        'pressure_psi': item.ZtestPrValPsi,
                        'unit': item.ZtestDurUnit
                    })

            return {
                'status': 'success',
                'valve_details': valve_data,
                'trace_details': trace_details,
                'tests': tests
            }
        else:
            reason = response.EpExcmsg if response.EpExcmsg else "Serial number not found in SAP."
            return {'status': 'error', 'message': reason}

    except Exception as e:
        return {'status': 'error', 'message': f'SAP Connection failed: {str(e)}'}


