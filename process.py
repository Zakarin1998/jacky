import subprocess

def convert_to_pdfa(input_pdf, output_pdf):
    gs_command = [
        'gs',
        '-dPDFA=1',
        '-dBATCH',
        '-dNOPAUSE',
        '-dNOOUTERSAVE',
        '-sProcessColorModel=DeviceCMYK',
        '-sDEVICE=pdfwrite',
        '-sPDFACompatibilityPolicy=1',
        f'-sOutputFile={output_pdf}',
        input_pdf
    ]
    try:
        subprocess.run(gs_command, check=True)
        print(f'Conversione completata: {output_pdf}')
    except subprocess.CalledProcessError as e:
        print(f'Errore nella conversione: {e}')

# Esempio di uso
input_pdf = 'doc_og.pdf'
output_pdf = 'doc_og_new.pdf'
convert_to_pdfa(input_pdf, output_pdf)
