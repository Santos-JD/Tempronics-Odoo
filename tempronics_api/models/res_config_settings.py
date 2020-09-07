class TempronicsApiSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_trics_api_mrp_produccion = fields.Boolean(_("Activar mrp_produccion"))
    module_trics_api_mrp_produccion_url = fields.Float(related='company_id.po_lead')


            
