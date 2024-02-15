from pydantic import BaseModel
from typing import Optional, List
from model.company import Company

from schemas import CommentSchema


class CompanySchema(BaseModel):
    # Defines how the fields should be represented when inserting a new company
    
    company_name: str = "Alpargatas S.A"
    trading_name: str = "Havaianas"
    cnpj: str = "99.999.999/0001-99"
    contact_name: str = "José da Silva"
    phone: str = "() 99999-9999"
    email: str = "josedasilva@seuemail.com"

    
class CompanySearchSchema(BaseModel):
    """ Defines how the structure representing the search that will be made based only on the "company_name" of the Company should be. """
    
    company_name: str = "Test"


class CompanyListSchema(BaseModel):
    # Defines how a list of companies will be returned.

    companies: List[CompanySchema]


def show_companies(companies: List[Company]):
    # Returns the representation of the company following the schema defined in "CompanyViewSchema".
  
    result = []
    for company in companies:
        result.append({
            "company_name": company.company_name,
            "trading_name": company.trading_name,
            "cnpj": company.cnpj,
            "contact_name": company.contact_name,
            "phone": company.phone,
            "email": company.email
        })

    return {"companies": result}


class CompanyViewSchema(BaseModel):
    # Defines how a company will be returned: company + comments

    id: int = 1
    company_name: str = "Alpargatas S.A"
    trading_name: str = "Havaianas"
    cnpj: str = "99.999.999/0001-99"
    contact_name: str = "José da Silva"
    phone: str = "() 99999-9999"
    email: str = "josedasilva@seuemail.com"
    total_comments: int = 1
    comments: List[CommentSchema]


class CompanyDeleteSchema(BaseModel):
    # Defines the structure of the data returned after a deletion request.

    message: str
    company_name: str

def show_company(company: Company):
    # Returns a representation of the company following the schema defined in CompanyViewSchema.

    return {
        "id": company.id,
        "company_name": company.company_name,
        "trading_name": company.trading_name,
        "cnpj": company.cnpj,
        "contact_name": company.contact_name,
        "phone": company.phone,
        "email": company.email,
        "total_comments": len(company.comments),
        "comments": [{"text": c.text} for c in company.comments]
    }
