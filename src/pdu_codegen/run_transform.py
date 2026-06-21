import os

import lxml.etree as ET


def run_xlst_transform(filepath_xml, filepath_xslt, filepath_output):
    dom = ET.parse(filepath_xml)
    xslt = ET.parse(filepath_xslt)
    transform = ET.XSLT(xslt)
    result = transform(dom)

    with open(filepath_output, 'w', encoding='utf-8') as f:
        f.write(str(result))


if __name__ == "__main__":
    filepath_dis_spec = "dis-description/DIS7.xml"

    # @PDU Model code generation, IMPL_DIS_PDU_MODEL_GENERATION, code_impl, [SPEC_PDU_CODE_GENERATION]
    run_xlst_transform(
        filepath_dis_spec,
        'pdu_to_django.xslt',
        os.path.join("..", "board", "pdu_models.py")
    )
    print(f"Generated pdu_models.py from {filepath_dis_spec} using XSLT.")

    # @PDU Detail view content generation, IMPL_DIS_PDU_DETAIL_GENERATION, code_impl, [SPEC_PDU_CODE_GENERATION]
    run_xlst_transform(
        filepath_dis_spec, 
        "pdu_to_detail.xslt",
        os.path.join("..", "board", "templates", "pdus", "partial_pdu_detail.html")
    )
    print(f"Generated partial_pdu_detail.html from {filepath_dis_spec} using XSLT.")


