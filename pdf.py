import asyncio
import os

import pdfplumber
from collections import defaultdict



async def pdf_parcer1(pdf_path: str, answer: defaultdict) -> bool:
    module = 0
    try:
        with pdfplumber.open(pdf_path) as pdf:
            name = ''
            for page in pdf.pages:
                text = page.extract_text()
                lines = text.split('\n')
                for line in lines:
                    if line == 'Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде':
                        module = 0
                        continue
                    if line == 'Настоящая выписка содержит сведения о юридическом лице':
                        module = 3
                        continue
                    elif line == 'полное наименование юридического лица':
                        module = 0
                        answer['NAME1'] = name
                        continue
                    elif line == 'Сведения о лице, имеющем право без доверенности действовать от имени юридического':
                        module = 1
                        continue
                    elif line == 'Сведения об участниках / учредителях юридического лица':
                        module = 2
                        continue
                    elif line == 'Сведения об учете в налоговом органе':
                        break
                    elif module == 3:
                        name += line + ' '
                    elif module == 1:
                        if "ИНН" in line :
                            if answer['ИНН_DIR1'] == '-':
                                answer['ИНН_DIR1'] = [line.split()[-1], ]
                            else:
                                answer['ИНН_DIR1'].append(line.split()[-1])
                    elif module == 2:
                        if "ИНН" in line:
                            if answer['ИНН_OWN1'] == '-':
                                answer['ИНН_OWN1'] = [line.split()[-1], ]
                            else:
                                answer['ИНН_OWN1'].append(line.split()[-1])

    except FileNotFoundError:
        os.remove(pdf_path)
        return False
    finally:
        os.remove(pdf_path)
        return True


async def pdf_parcer2(pdf_path: str, answer: defaultdict) -> bool:
    module = 0
    try:
        with pdfplumber.open(pdf_path) as pdf:
            name = ''
            for page in pdf.pages:
                text = page.extract_text()
                lines = text.split('\n')
                for line in lines:
                    if line == 'Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде':
                        module = 0
                        continue
                    if line == 'Настоящая выписка содержит сведения о юридическом лице':
                        module = 3
                        continue
                    elif line == 'полное наименование юридического лица':
                        module = 0
                        answer['NAME1'] = name
                        continue
                    elif line == 'Сведения о лице, имеющем право без доверенности действовать от имени юридического':
                        module = 1
                        continue
                    elif line == 'Сведения об участниках / учредителях юридического лица':
                        module = 2
                        continue
                    elif line == 'Сведения об учете в налоговом органе':
                        break
                    elif module == 3:
                        name += line + ' '
                    elif module == 1:
                        if "ИНН" in line and answer['ИНН_DIR2'] == '-':
                            answer['ИНН_DIR2'] = line.split()[-1]
                    elif module == 2:
                        if "ИНН" in line:
                            if answer['ИНН_OWN2'] == '-':
                                answer['ИНН_OWN2'] = [line.split()[-1], ]
                            else:
                                answer['ИНН_OWN2'].append(line.split()[-1])

    except FileNotFoundError:
        os.remove(pdf_path)
        return False
    finally:
        os.remove(pdf_path)
        return True
