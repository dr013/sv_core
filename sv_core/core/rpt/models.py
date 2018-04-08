from django.db import models
from django.utils.translation import ugettext_lazy as _


class Report(models.Model):
    """Reports hierarchy."""

    class Meta:
        db_table = 'rpt_report'
        verbose_name = _("Report")

    name = models.CharField(_("Report name"), max_length=200, help_text=_("Report name"))
    data_source = models.CharField(_("Report source(SQL)"), max_length=4000,
                                   help_text=_("Report source (SQL command)."))
    source_type = models.CharField(_("Source type"), max_length=8,
                                   help_text=_("Data source type (plain data, XML, refcursor)."))


class Template(models.Model):
    """Report template. Markdown format."""

    class Meta:
        db_table = "rpt_template"
        verbose_name = _("Template")

    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True, help_text=_("Reference to report."))
    lang = models.CharField(_("Language"), max_length=8,help_text=_("Multi language template support."), default='LANGRUS')
    text = models.TextField(_("Text"), help_text=_("Template source."))
    base64 = models.TextField(_("Base64"), help_text=_("Encoded text"), editable=False)
    report_processor = models.CharField(_("Report processor"), max_length=8, help_text=_("Report processor."))
    report_format = models.CharField(_("Report format"), max_length=8, help_text=_("Report file format."))
