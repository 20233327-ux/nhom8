import os
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers
from pyhanko.sign.fields import SigFieldSpec, append_signature_field
from vn_docs.models import Document
from django.conf import settings

def sign_pdf_document(doc_id, p12_file_path, passphrase, reason="Phê duyệt công văn"):
    """
    Ký số lên file PDF bằng chứng thư số (.p12)
    """
    try:
        doc = Document.objects.get(id=doc_id)
        input_path = doc.file_attachment.path
        output_filename = f"signed_{os.path.basename(input_path)}"
        output_path = os.path.join(os.path.dirname(input_path), output_filename)

        # Load signer từ file .p12
        signer = signers.P12Signer(
            p12_file=p12_file_path,
            passphrase=passphrase.encode()
        )

        with open(input_path, 'rb') as inf:
            w = IncrementalPdfFileWriter(inf)
            # Thêm trường ký tên vào PDF
            append_signature_field(
                w, SigFieldSpec(sig_field_name='Signature1', on_page=0, box=(100, 100, 300, 200))
            )

            with open(output_path, 'wb') as outf:
                signers.sign_pdf(
                    w, signers.PdfSignatureMetadata(field_name='Signature1', reason=reason),
                    signer=signer, output=outf,
                )
        
        # Cập nhật đường dẫn file đã ký vào database (tùy chọn lưu đè hoặc lưu bản mới)
        # Ở đây chúng ta ví dụ là cập nhật trạng thái
        doc.status = 'signed'
        doc.save()
        
        return True, output_path
    except Exception as e:
        return False, str(e)
