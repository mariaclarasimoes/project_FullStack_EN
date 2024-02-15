from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Company, Comment
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="My API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definition of tags
home_tag = Tag(name="Documentation", description="Selection of documentation: Swagger, Redoc, or RapiDoc")
company_tag = Tag(name="Company", description="Addition, visualization, and removal of companies from the database")
comment_tag = Tag(name="Comment", description="Adding a comment to a company registered in the database")


@app.get('/', tags=[home_tag])
def home():
    """Redirects to /openapi, screen that allows choosing the documentation style."""
    
    return redirect('/openapi')


@app.post('/company', tags=[company_tag],
          responses={"200": CompanyViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_company(form: CompanySchema):
    """Adds a new company to the database
    Returns a representation of the companies and associated comments."""

    company = Company(
        company_name=form.company_name,
        trading_name=form.trading_name,
        cnpj=form.cnpj,
        contact_name= form.contact_name,
        phone= form.phone,
        email=form.email
        )
    logger.debug(f"Adding a company named: '{company.company_name}'")
    try:
        # Creating connection to the database
        session = Session()
        # Adding company
        session.add(company)
        # Committing the command to add a new item to the table
        session.commit()
        logger.debug(f"Added company named: '{company.company_name}'")
        return show_company(company), 200

    except IntegrityError as e:
        # Duplicity of company_name is likely reason for IntegrityError
        error_msg = "Company with the same name already saved in the database"
        logger.warning(f"Error adding company '{company.company_name}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # If another error occurs outside the expected
        error_msg = "Could not save new item"
        logger.warning(f"Error adding company '{company.company_name}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/companies', tags=[company_tag],
         responses={"200": CompanyListSchema, "404": ErrorSchema})
def get_companies():
    """Searches for all registered companies. 
    Returns a representation of the list of companies.
    """
    logger.debug(f"Collecting companies ")
    # Creating connection to the database
    session = Session()
    # Searching
    companies = session.query(Company).all()

    if not companies:
        # Checks if there are no registered companies
        return {"companies": []}, 200
    else:
        logger.debug(f"{len(companies)} Companies found: ")
        # Returns the representation of the company
        print(companies)
        return show_companies(companies), 200


@app.delete('/company', tags=[company_tag],
            responses={"200": CompanyDeleteSchema, "404": ErrorSchema})
def del_company(query: CompanySearchSchema):
    """Deletes a company based on the informed "company_name"
    Returns a confirmation message of the removal. """
    company_company_name = unquote(unquote(query.company_name))
    print(company_company_name)
    logger.debug(f"Deleting data about company #{company_company_name}")

    # Creating connection to the database
    session = Session()

    # Making the removal
    count = session.query(Company).filter(Company.company_name == company_company_name).delete()
    session.commit()

    if count:
        # Returns the representation of the confirmation message
        logger.debug(f"Company deleted: #{company_company_name}")
        return {"message": "Company removed", "id": company_company_name}
    else:
        # If the company was not found
        error_msg = "Company not found in the database"
        logger.warning(f"Error deleting company '#{company_company_name}', {error_msg}")
        return {"message": error_msg}, 404


@app.post('/comment', tags=[comment_tag],
          responses={"200": CompanyViewSchema, "404": ErrorSchema})
def add_comment(form: CommentSchema):
    """Adds a new comment to the company registered in the database identified by id
    Returns a representation of the companies and associated comments. """
    company_id  = form.company_id
    logger.debug(f"Adding comments to company #{company_id}")

    # Creating connection to the database
    session = Session()
    # Searching for the company
    company = session.query(Company).filter(Company.id == company_id).first()

    if not company:
        # If the company is not found
        error_msg = "Company not found in the database"
        logger.warning(f"Error adding comment to company '{company_id}', {error_msg}")
        return {"message": error_msg}, 404

    # Creating the comment
    text = form.text
    comment = Comment(text)

    # Adding comment to the company
    company.add_comment(comment)
    session.commit()

    logger.debug(f"Comment added to company #{company_id}")

    # Returns the representation of the company
    return show_company(company), 200
