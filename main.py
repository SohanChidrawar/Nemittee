''' Process the Tally Daybook XML files and make a spreadsheet with the given format.
Tally allows the users to download XML files that contain information about the transactions. We are providing you with one such file. Study the input file, and create a 
response spreadsheet for all the transactions where the voucher type is “Receipt”.

Input:
- An XML file.
End result:
- Response .xls or .xlsx file.
'''

from flask import Flask, request, jsonify
import pandas as pd
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    xml_file = request.files.get('xml_file')
    if not xml_file:
        return jsonify({'error': 'XML file not found.'}), 400

    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = []
    for child in root.findall('VOUCHER'):
        vch_type = child.attrib.get('VCHTYPE')
        if vch_type != 'Receipt':
            continue

        vch_number = child.attrib.get('VOUCHERNUMBER')
        date = child.find('DATE').text
        party_name = child.find('PARTYLEDGERNAME').text
        amount = child.find('ALLLEDGERENTRIES.LIST').find('AMOUNT').text
        data.append({
            'VoucherType': vch_type,
            'VoucherNumber': vch_number,
            'Date': date,
            'PartyName': party_name,
            'Amount': amount
        })

    if not data:
        return jsonify({'error': 'No Receipt Vouchers found.'}), 400

    df = pd.DataFrame(data)
    writer = pd.ExcelWriter('receipts.xlsx')
    df.to_excel(writer, index=False)
    writer.save()

    return jsonify({'success': 'Excel file created.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
