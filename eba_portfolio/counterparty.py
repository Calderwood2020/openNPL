# Copyright (c) 2020 Open Risk (https://www.openriskmanagement.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from django.db import models
from django.urls import reverse

from eba_portfolio.models import Portfolio_Snapshot, Portfolio

"""
Data object holds Counterparty Portfolio data conforming to the EBA NPL Template specification
`EBA Templates <https://www.openriskmanual.org/wiki/EBA_NPL_Template>`_


"""


class Counterparty(models.Model):
    #
    # CHOICE DICTIONARIES
    #

    COUNTERPARTY_ROLE_CHOICES = [(0, '(a) Guarantor'), (1, '(b) Borrower'), (2, '(c) Tenant')]

    LEGAL_TYPE_OF_COUNTERPARTY_CHOICES = [
        (0, '(a) Listed Corporate is a Corporate entity whose shares are quoted and traded on a Stock Exchange'),
        (1, '(b) Unlisted Corporate is a Corporate entity whose shares are not quoted and traded on a stock exchange, '
            'however an unlisted corporate may have an unlimited number of shareholders to raise capital for any '
            'commercial venture'),
        (2, '(c) Listed Fund is a fund whose shares are quoted and traded on a Stock exchange'),
        (3, '(d) Unlisted Fund is a fund whose shares are not quoted and traded on a Stock exchange'),
        (4, '(e) Partnership is where the Sponsor constitutes a group of individuals who form a legal partnership, '
            'where profits and liabilities are shared; or,'),
        (5, '(f) Private Individual')]

    TYPE_OF_PERSONAL_IDENTITY_NUMBER_CHOICES = [(0, '(a) Passport Number'), (1, '(b) National Insurance Number'),
                                                (2, '(c) National tax number'), (3, '(d) Other')]

    NATIONALITY_OF_COUNTERPARTY_CHOICES = [(0, 'REF: ISO 20022')]

    CITY_OF_RESIDENCE_CHOICES = [(0, 'REF: UN/LOCODE')]

    GEOGRAPHIC_REGION_OF_RESIDENCE_CHOICES = [(0, 'REF: NUTS3')]

    GEOGRAPHIC_REGION_CLASSIFICATION_CHOICES = [(0, '(a) NUTS3 2013'), (1, '(b) NUTS3 2010'), (2, '(c) NUTS3 2006'),
                                                (3, '(d) NUTS3 2003'), (4, '(e) Other')]

    COUNTRY_OF_RESIDENCE_CHOICES = [(0, 'REF: ISO 3166 ALPHA-2')]

    CURRENCY_OF_ANNUAL_INCOME_CHOICES = [(0, 'REF: ISO 4217')]

    EMPLOYMENT_STATUS_CHOICES = [(0, '(a) Employed'), (1, '(b) Employed with partial support (company subsidy)'),
                                 (2, '(c) Protected life-time employment (civil servant)'), (3, '(d) Self-employed'),
                                 (4, '(e) Unemployed'), (5, '(f) Student'), (6, '(g) Pensioner'), (7, '(h) Other')]

    OCCUPATION_TYPE_CHOICES = [(0, 'REF: ISCO-08')]

    LEGAL_entity_idENTIFIER_CHOICES = [(0, 'REF: ISO 17442 LEI')]

    CITY_OF_REGISTERED_LOCATION_CHOICES = [(0, 'REF: UN/LOCODE')]

    GEOGRAPHIC_REGION_OF_REGISTERED_LOCATION_CHOICES = [(0, 'REF: NUTS3')]

    COUNTRY_OF_REGISTERED_LOCATION_CHOICES = [(0, 'REF: ISO 3166 ALPHA-2')]

    BASIS_OF_FINANCIAL_STATEMENTS_CHOICES = [(0, '(a) IFRS'), (1, '(b) National GAAP '), (2, '(c) Other')]

    FINANCIAL_STATEMENTS_TYPE_CHOICES = [(0, '(a) Consolidated'), (1, '(b) Counterparty level')]

    CURRENCY_OF_FINANCIAL_STATEMENTS_CHOICES = [(0, 'REF: ISO 4217')]

    ENTERPRISE_SIZE_CHOICES = [(0, '(a) Micro-enterprise'), (1, '(b) Small enterprise'), (2, '(c) Medium enterprise'),
                               (3, '(d) Large enterprise')]

    INDUSTRY_SEGMENT_CHOICES = [(0, 'REF: NACE')]

    CROSS_DEFAULT_FOR_COUNTERPARTY_CHOICES = [(0, '(a) Full'), (1, '(b) Partial'), (2, '(c) None')]

    CROSS_COLLATERALISATION_FOR_COUNTERPARTY_CHOICES = [(0, '(a) Full'), (1, '(b) Partial'), (2, '(c) None')]

    CURRENCY_OF_DEPOSIT_CHOICES = [(0, 'REF: ISO 4217')]

    LEGAL_STATUS_CHOICES = [
        (0, '(a) Listed Corporate is a Corporate entity whose shares are quoted and traded on a Stock Exchange'),
        (1, '(b) Unlisted Corporate is a Corporate entity whose shares are not quoted and traded on a stock exchange, '
            'however an unlisted corporate may have an unlimited number of shareholders to raise capital for any '
            'commercial venture'),
        (2, '(c) Listed Fund is a fund whose shares are quoted and traded on a Stock exchange'),
        (3, '(d) Unlisted Fund is a fund whose shares are not quoted and traded on a Stock exchange'),
        (4, '(e) Partnership is where the Sponsor constitutes a group of individuals who form a legal partnership, '
            'where profits and liabilities are shared; or,'),
        (5, '(f) Private Individual')]

    LEGAL_PROCEDURE_TYPE_CHOICES = [(0, '(a) Corporate Restructuring Procedures, which also include funds'),
                                    (1, '(b) Corporate Insolvency Procedures, which also include funds'),
                                    (2, '(c) Private Individual Counterparty Debt Compromise Procedures'),
                                    (3, '(d) Private Individual Counterparty Insolvency Procedures'),
                                    (4, '(e) Partnership Restructuring Procedures'),
                                    (5, '(f) Partnership Insolvency Procedures')]

    LEGAL_PROCEDURE_NAME_CHOICES = [(0, 'Country Specific: Annex I')]

    JURISDICTION_OF_COURT_CHOICES = [(0, 'REF: ISO 3166 ALPHA-2')]

    #
    # EBA TEMPLATE FIELDS
    #

    counterparty_identifier = models.TextField(unique=True,
                                               help_text='Unique internal identifier for the Counterparty. One or multiple Counterparties can be part of a Counterparty. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Counterparty_Identifier">Documentation</a>'
                                               )
    address_of_registered_location = models.TextField(blank=True, null=True,
                                                      help_text='Address where the Corporate Counterparty is registered,'
                                                                ' including flat / house number. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Address_of_Registered_Location">Documentation</a>'
                                                      )
    annual_ebit = models.BigIntegerField(blank=True, null=True,
                                         help_text='Amount of annual EBIT held by the Corporate Counterparty as per the '
                                                   'latest available financial statements. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Annual_EBIT">Documentation</a>'
                                         )
    annual_revenue = models.BigIntegerField(blank=True, null=True,
                                            help_text='Amount of annual revenue held by the Corporate Counterparty as per the latest available financial statements. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Annual_Revenue">Documentation</a>'
                                            )
    basis_of_financial_statements = models.IntegerField(blank=True, null=True,
                                                        choices=BASIS_OF_FINANCIAL_STATEMENTS_CHOICES,
                                                        help_text='Financial reporting practice the Corporate Counterparty has adopted i.e. IFRS, National GAAP, Not Available. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Basis_of_Financial_Statements">Documentation</a>'
                                                        )
    business_description = models.TextField(blank=True, null=True,
                                            help_text='Description of the business operations of the Corporate Counterparty, providing more detail for field "Industry Segment". <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Business_Description">Documentation</a>'
                                            )
    cash_and_cash_equivalent_items = models.BigIntegerField(blank=True, null=True,
                                                            help_text='Amount of cash and cash equivalent items held by the Corporate Counterparty as  per the latest available financial statements. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Cash_and_Cash_Equivalent_Items">Documentation</a>'
                                                            )
    city_of_registered_location = models.IntegerField(blank=True, null=True,
                                                      choices=CITY_OF_REGISTERED_LOCATION_CHOICES,
                                                      help_text='City where the Corporate Counterparty is registered. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.City_of_Registered_Location">Documentation</a>'
                                                      )
    comments_on_other_litigation_related_process = models.TextField(blank=True, null=True,
                                                                    help_text='Further comments / details if there is other litigation processes in place. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Comments_on_Other_Litigation_Related_Process">Documentation</a>'
                                                                    )
    contingent_obligations = models.TextField(blank=True, null=True,
                                              help_text='Indicator as to whether the Corporate Counterparty has contingent obligations which will be part of the sale, e.g. the Institution provided a guarantee to a real estate developer on their development. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Contingent_Obligations">Documentation</a>'
                                              )
    counterparty_group_identifier = models.TextField(blank=True, null=True,
                                                     help_text='Institutions internal identifier for the Counterparty Group. Where Counterparty Group is defined as a group of related Counterparties. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Counterparty_Group_Identifier">Documentation</a>'
                                                     )
    counterparty_role = models.IntegerField(blank=True, null=True, choices=COUNTERPARTY_ROLE_CHOICES,
                                            help_text='Type of the Counterparty i.e. Guarantor, Borrower, Tenant. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Counterparty_Role">Documentation</a>'
                                            )
    country_of_registered_location = models.IntegerField(blank=True, null=True,
                                                         choices=COUNTRY_OF_REGISTERED_LOCATION_CHOICES,
                                                         help_text='Country where the Corporate Counterparty is registered. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Country_of_Registered_Location">Documentation</a>'
                                                         )
    cross_collateralisation_for_counterparty = models.IntegerField(blank=True, null=True,
                                                                   choices=CROSS_COLLATERALISATION_FOR_COUNTERPARTY_CHOICES,
                                                                   help_text='Indicator as to whether all / some of the loans held by the Counterparty are secured by all / some of the collaterals held by the Counterparty. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Cross_Collateralisation_for_Counterparty">Documentation</a>'
                                                                   )
    cross_default_for_counterparty = models.IntegerField(blank=True, null=True,
                                                         choices=CROSS_DEFAULT_FOR_COUNTERPARTY_CHOICES,
                                                         help_text='Indicator as to whether contractual breach of any loans held by the Counterparty would trigger the default event of any other loans. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Cross_Default_for_Counterparty">Documentation</a>'
                                                         )
    currency_of_deposit = models.IntegerField(blank=True, null=True, choices=CURRENCY_OF_DEPOSIT_CHOICES,
                                              help_text='Currency that the deposit held with the Institution is expressed in. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Currency_of_Deposit">Documentation</a>'
                                              )
    currency_of_financial_statements = models.IntegerField(blank=True, null=True,
                                                           choices=CURRENCY_OF_FINANCIAL_STATEMENTS_CHOICES,
                                                           help_text='Currency that the latest available financial statements are expressed in. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Currency_of_Financial_Statements">Documentation</a>'
                                                           )
    current_assets = models.BigIntegerField(blank=True, null=True,
                                            help_text='Amount of current assets held by the Corporate Counterparty, excluding cash and cash equivalent items as per the latest available financial statements. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Current_Assets">Documentation</a>'
                                            )
    current_external_credit_rating = models.TextField(blank=True, null=True,
                                                      help_text='External credit rating issued to the Corporate Counterparty at NPL Portfolio Cut-Off Date. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Current_External_Credit_Rating">Documentation</a>'
                                                      )
    current_internal_credit_rating = models.TextField(blank=True, null=True,
                                                      help_text='Internal credit rating issued to the Counterparty at the NPL Portfolio Cut-Off Date and please provide the internal methodology used to decide the rating as a part of the transaction documents. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Current_Internal_Credit_Rating">Documentation</a>'
                                                      )
    date_of_appointment = models.DateField(blank=True, null=True,
                                           help_text='Date that the insolvency practitioner was appointed. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Date_of_Appointment">Documentation</a>'
                                           )
    date_of_entering_into_current_legal_process = models.DateField(blank=True, null=True,
                                                                   help_text='Date that the Counterparty entered into their current legal status. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Date_of_Entering_Into_Current_Legal_Process">Documentation</a>'
                                                                   )
    date_of_external_demand_issuance = models.DateField(blank=True, null=True,
                                                        help_text='Date that a demand notice was sent by solicitors who act on behalf of the Institution. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Date_of_External_Demand_Issuance">Documentation</a>'
                                                        )
    date_of_incorporation = models.DateField(blank=True, null=True,
                                             help_text='Date that the Corporate Counterparty was incorporated as a company, partnership or fund, and therefore became a separate legal entity from its owners, with its own rights and obligations. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Date_of_Incorporation">Documentation</a>'
                                             )
    date_of_internal_demand_issuance = models.DateField(blank=True, null=True,
                                                        help_text='Date that a demand notice was sent by the Institution itself. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Date_of_Internal_Demand_Issuance">Documentation</a>'
                                                        )
    date_of_last_contact = models.DateField(blank=True, null=True,
                                            help_text='Date of last direct contact with the Counterparty. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Date_of_Last_Contact">Documentation</a>'
                                            )
    date_of_latest_annual_financial_statements = models.DateField(blank=True, null=True,
                                                                  help_text='Date of the latest available Financial Statements. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Date_of_Latest_Annual_Financial_Statements">Documentation</a>'
                                                                  )
    date_of_obtaining_order_for_possession = models.DateField(blank=True, null=True,
                                                              help_text='Date that the Order for Possession is granted by the court. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Date_of_Obtaining_Order_for_Possession">Documentation</a>'
                                                              )
    date_when_reservation_of_rights_letter_was_issued = models.DateField(blank=True, null=True,
                                                                         help_text='Date that the Reservation of Rights Letter was issued by the Institution. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Date_when_Reservation_of_Rights_Letter_Was_Issued">Documentation</a>'
                                                                         )
    deposit_balance_with_institution = models.BigIntegerField(blank=True, null=True,
                                                              help_text='Deposit amount the Counterparty holds with the Institution as defined by annex II, Part two of the ECB BSI Regulation. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Deposit_Balance_with_Institution">Documentation</a>'
                                                              )
    description_of_contingent_obligations = models.TextField(blank=True, null=True,
                                                             help_text='Description of contingent obligations when "Yes" is selected in field "Contingent Obligations". <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Description_of_Contingent_Obligations">Documentation</a>'
                                                             )
    description_of_cross_collateralisation = models.TextField(blank=True, null=True,
                                                              help_text='Description of cross collateralisation when "Partial" is selected in field "Cross Collateralisation for Counterparty". <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Description_of_Cross_Collateralisation">Documentation</a>'
                                                              )
    description_of_cross_default = models.TextField(blank=True, null=True,
                                                    help_text='Description of cross default when "Partial" is selected in field "Cross Default for Counterparty". <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Description_of_Cross_Default">Documentation</a>'
                                                    )
    description_of_related_party = models.TextField(blank=True, null=True,
                                                    help_text='Further comments / details on the nature of the relation between the institution and the related party when "Yes" is selected in field "Related Party". <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Description_of_Related_Party">Documentation</a>'
                                                    )
    eligibility_for_deposit_to_offset = models.TextField(blank=True, null=True,
                                                         help_text='Indicator as to whether the deposit held with the Institution can be used to pay down the loan. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Eligibility_for_Deposit_to_Offset">Documentation</a>'
                                                         )
    enterprise_size = models.IntegerField(blank=True, null=True, choices=ENTERPRISE_SIZE_CHOICES,
                                          help_text='Classification of enterprises by size for the Corporate Counterparty i.e. Microenterprise, Small enterprise, Medium enterprise and Large enterprise. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Enterprise_Size">Documentation</a>'
                                          )
    eviction_date = models.DateField(blank=True, null=True,
                                     help_text='Date that the Counterparty is evicted. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Eviction_Date">Documentation</a>'
                                     )
    external_credit_rating_at_origination = models.TextField(blank=True, null=True,
                                                             help_text='External credit rating issued to the Corporate Counterparty applicable at the point in time when the Counterparty became a customer and choose the lowest one if there are multiple ratings. In case several ratings are assigned, the approach described in Art. 138 of the CRR applies.. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.External_Credit_Rating_at_Origination">Documentation</a>'
                                                             )
    financial_statements_type = models.IntegerField(blank=True, null=True, choices=FINANCIAL_STATEMENTS_TYPE_CHOICES,
                                                    help_text='Indicator as to whether the financial statements have been prepared at the Consolidated or at the Counterparty level. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Financial_Statements_Type">Documentation</a>'
                                                    )
    financials_audited = models.TextField(blank=True, null=True,
                                          help_text='Indicator as to whether the financial statements have been audited or not by the Corporate Counterparty. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Financials_Audited">Documentation</a>'
                                          )
    fixed_assets = models.BigIntegerField(blank=True, null=True,
                                          help_text='Amount of fixed assets held by the Corporate Counterparty as per the latest available financial statements. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Fixed_Assets">Documentation</a>'
                                          )
    geographic_region_classification = models.IntegerField(blank=True, null=True,
                                                           choices=GEOGRAPHIC_REGION_CLASSIFICATION_CHOICES,
                                                           help_text='NUTS3 classification used for the field "Geographic Region of Registered Location", i.e. NUTS3 2013 (1), NUTS3 2010 (2), NUTS3 2006 (3), NUTS3 2003 (4), Other (5). <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Geographic_Region_Classification">Documentation</a>'
                                                           )
    geographic_region_of_registered_location = models.IntegerField(blank=True, null=True,
                                                                   choices=GEOGRAPHIC_REGION_OF_REGISTERED_LOCATION_CHOICES,
                                                                   help_text='Province or Region where the Corporate Counterparty is registered. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Geographic_Region_of_Registered_Location">Documentation</a>'
                                                                   )
    indicator_of_counterparty_cooperation = models.TextField(blank=True, null=True,
                                                             help_text='Indicator as to whether the Corporate or Private Individual Counterparty is cooperative or not. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Indicator_of_Counterparty_Cooperation">Documentation</a>'
                                                             )
    industry_segment = models.IntegerField(blank=True, null=True, choices=INDUSTRY_SEGMENT_CHOICES,
                                           help_text='Industry in which the Corporate Counterparty mainly operates. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Industry_Segment">Documentation</a>'
                                           )
    insolvency_practitioner_appointed = models.TextField(blank=True, null=True,
                                                         help_text='Indicator as to whether an insolvency practitioner has been appointed. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Insolvency_Practitioner_Appointed">Documentation</a>'
                                                         )
    internal_credit_rating_at_origination = models.TextField(blank=True, null=True,
                                                             help_text='Internal credit rating issued to the Counterparty applicable at the point in time when the Counterparty became a customer. Please provide the internal methodology used to decide the rating as a part of the transaction documents. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Internal_Credit_Rating_at_Origination">Documentation</a>'
                                                             )
    jurisdiction_of_court = models.IntegerField(blank=True, null=True, choices=JURISDICTION_OF_COURT_CHOICES,
                                                help_text='Location of the court where the case is being heard. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Jurisdiction_of_Court">Documentation</a>'
                                                )
    legal_actions_completed = models.TextField(blank=True, null=True,
                                               help_text='Description of the legal actions completed for the Counterparty. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Legal_Actions_Completed">Documentation</a>'
                                               )
    legal_entity_identifier = models.TextField(blank=True, null=True, choices=LEGAL_entity_idENTIFIER_CHOICES,
                                               help_text='Global standard 20-character corporate identifier of the Corporate Counterparty. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Legal_entity_identifier">Documentation</a>'
                                               )
    legal_fees_accrued = models.BigIntegerField(blank=True, null=True,
                                                help_text='Total amount of legal fees accrued at the NPL Portfolio Cut-Off Date. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Legal_Fees_Accrued">Documentation</a>'
                                                )
    legal_procedure_name = models.IntegerField(blank=True, null=True, choices=LEGAL_PROCEDURE_NAME_CHOICES,
                                               help_text='Name of the legal procedure which provides an indication of how advanced the relevant procedure has become, depending on the country where the Counterparty is located. choice fields indicate country specifics features). <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Legal_Procedure_Name">Documentation</a>'
                                               )
    legal_procedure_type = models.IntegerField(blank=True, null=True, choices=LEGAL_PROCEDURE_TYPE_CHOICES,
                                               help_text='Type of the insolvency process the Counterparty is currently in. Choice fields are provided indicating per country the possible procedures. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Legal_Procedure_Type">Documentation</a>'
                                               )
    legal_status = models.IntegerField(blank=True, null=True, choices=LEGAL_STATUS_CHOICES,
                                       help_text='The type of legal status of the Counterparty. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Legal_status">Documentation</a>'
                                       )
    legal_type_of_counterparty = models.IntegerField(blank=True, null=True, choices=LEGAL_TYPE_OF_COUNTERPARTY_CHOICES,
                                                     help_text='Type of the Counterparty i.e. Private Individual, Listed Corporate, Unlisted Corporate and Partnership. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Legal_Type_of_Counterparty">Documentation</a>'
                                                     )
    market_capitalisation = models.BigIntegerField(blank=True, null=True,
                                                   help_text='Market capitalisation of a listed Corporate Counterparty. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Market_Capitalisation">Documentation</a>'
                                                   )
    name_of_counterparty = models.TextField(blank=True, null=True,
                                            help_text='Name used to refer to the Counterparty. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Name_of_Counterparty">Documentation</a>'
                                            )
    name_of_insolvency_practitioner = models.TextField(blank=True, null=True,
                                                       help_text='Name of the insolvency practitioner. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Name_of_Insolvency_Practitioner">Documentation</a>'
                                                       )
    net_assets = models.BigIntegerField(blank=True, null=True,
                                        help_text='Amount of net assets held by the Corporate Counterparty as per the latest available financial statements. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Net_Assets">Documentation</a>'
                                        )
    number_of_fte = models.BigIntegerField(blank=True, null=True,
                                           help_text='Number of full-time employees (or equivalent) working for the Corporate Counterparty as at the last financial reporting date. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Number_of_FTE">Documentation</a>'
                                           )
    number_of_joint_counterparties = models.BigIntegerField(blank=True, null=True,
                                                            help_text='Number of joint Counterparties who jointly own parts of the Loan.. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Number_of_Joint_Counterparties">Documentation</a>'
                                                            )
    other_products_with_institution = models.TextField(blank=True, null=True,
                                                       help_text='Other products that the Counterparty holds with the Institution that are not included in the NPL Portfolio. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Other_Products_with_Institution">Documentation</a>'
                                                       )
    postcode_of_registered_location = models.TextField(blank=True, null=True,
                                                       help_text='Postcode where the Corporate Counterparty is registered. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Postcode_of_Registered_Location">Documentation</a>'
                                                       )
    registration_number = models.TextField(blank=True, null=True,
                                           help_text='Company registration number of the Corporate Counterparty according to the country specific registration office. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Registration_number">Documentation</a>'
                                           )
    related_party = models.TextField(blank=True, null=True,
                                     help_text='Indicator as to whether the Counterparty is a related party to the Institution, e.g. Counterparty is an employee of the Institution. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Related_Party">Documentation</a>'
                                     )
    sheriff_or_bailiff_acquisition_date = models.DateField(blank=True, null=True,
                                                           help_text='Date that sheriff / bailiff is acquired by the court. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Sheriff_or_Bailiff_Acquisition_Date">Documentation</a>'
                                                           )
    source_of_current_external_credit_rating = models.TextField(blank=True, null=True,
                                                                help_text='Agency which provided the external credit rating at cut-off date. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Source_of_Current_External_Credit_Rating">Documentation</a>'
                                                                )
    source_of_external_credit_rating_at_origination = models.TextField(blank=True, null=True,
                                                                       help_text='From which agency the external credit rating at the point in time when the Counterparty became a customer. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Source_of_External_Credit_Rating_at_Origination">Documentation</a>'
                                                                       )
    total_assets = models.BigIntegerField(blank=True, null=True,
                                          help_text='Amount of total assets held by the Corporate Counterparty as per the latest available financial statements. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Total_Assets">Documentation</a>'
                                          )
    total_debt = models.BigIntegerField(blank=True, null=True,
                                        help_text='Amount of total debt held by the Corporate Counterparty as per the latest available financial statements. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Total_Debt">Documentation</a>'
                                        )
    total_liabilities = models.BigIntegerField(blank=True, null=True,
                                               help_text='Amount of total liabilities held by the Corporate Counterparty on the balance sheet as defined by the applicable accounting standard as per the latest available financial statements. <a class="risk_manual_url" href="https://www.openriskmanual.org/wiki/EBA_NPL.Counterparty.Total_Liabilities">Documentation</a>'
                                               )

    # Portfolio ID Foreign Key
    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True, help_text="The portfolio ID to which the Counterparty belongs (can be more than one)")

    # Snapshot ID  Foreign Key
    snapshot_id = models.OneToOneField(Portfolio_Snapshot, on_delete=models.CASCADE, blank=True, null=True, help_text="The snapshot ID to which the Counterparty belongs (must be unique)")


    # Bookkeeping Fields
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.counterparty_identifier

    def get_absolute_url(self):
        return reverse('eba_portfolio:eba_counterparty_edit', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Counterparty"
        verbose_name_plural = "Counterparties"