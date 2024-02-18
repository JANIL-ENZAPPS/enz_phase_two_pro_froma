# -*- coding: utf-8 -*-
{
    'name': "Enzapps Nactom Phase 2 Pro Froma",
    'author':
        'Enzapps',
    'summary': """
    This is a module is for Nactom Phase 2 Invoice Pro Froma
""",

    'description': """
        This is a module is for Phase 2 Invoice Pro Froma
    """,
    'website': "www.enzapps.com",
    'category': 'base',
    'version': '14.0',
    'depends': ['base', 'contacts', 'sale', 'sale_management', 'sale_stock', 'stock', 'product', 'account','account_invoice_ubl','natcomjson',
                'natcomsfeb_email_form', 'natcoms_jan_mou_enz','ksa_zatca_integration','enz_natcom_pahse_one_deactivate','natcom_api_phase_two','enz_natcom_sales_return_fix','natcom_phase_two_date_fix','pro_forma_invoice','arabic_number_update','natcom_prof_finals_april','natcom_proforma','pro_forma_currency_april','natcom_phase_two_date_fix_time_remove'],
    "images": ['static/description/icon.png'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/pro_forma_wiz.xml',
        'views/account_move.xml',
        'views/pro_forma.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
