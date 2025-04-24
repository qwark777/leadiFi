import asyncio
import os

import pdfplumber
from collections import defaultdict



async def pdf_parcer1(pdf_path: str, answer: defaultdict) -> bool:
    module = 0
    name = ''
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                lines = text.split('\n')
                for line in lines:
                    if line == 'Настоящая выписка содержит сведения о юридическом лице':
                        module = 3
                        continue
                    if line == 'полное наименование юридического лица':
                        module = 0
                        answer['NAME1'] = name
                        continue
                    if module == 3:
                        name += line + ' '
                    if line == 'Сведения о лице, имеющем право без доверенности действовать от имени юридического':
                        module = 1
                    if line == 'Сведения об участниках / учредителях юридического лица':
                        module = 2
                    if line == 'Сведения об учете в налоговом органе':
                        break
                    if module == 1:
                        if "ИНН" in line and answer['ИНН_DIR1'] == '-':
                            answer['ИНН_DIR1'] = line.split()[-1]
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
                    if line == 'Настоящая выписка содержит сведения о юридическом лице':
                        module = 3
                        continue
                    if line == 'полное наименование юридического лица':
                        module = 0
                        answer['NAME1'] = name
                        continue
                    if module == 3:
                        name += line + ' '
                    if line == 'Сведения о лице, имеющем право без доверенности действовать от имени юридического':
                        module = 1
                    if line == 'Сведения об участниках / учредителях юридического лица':
                        module = 2
                    if line == 'Сведения об учете в налоговом органе':
                        break
                    if module == 1:
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


