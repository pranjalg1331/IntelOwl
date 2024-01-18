# Generated by Django 4.2.8 on 2024-01-09 14:31
import django
from django.db import migrations, models


def migrate(apps, schema_editor):
    AnalyzerReport = apps.get_model("analyzers_manager", "AnalyzerReport")
    AnalyzerConfig = apps.get_model("analyzers_manager", "AnalyzerConfig")
    name = AnalyzerConfig.objects.filter(
        name=models.OuterRef("old_config")
    ).values_list("pk")[:1]
    AnalyzerReport.objects.update(config=models.Subquery(name))
    for config in AnalyzerConfig.objects.all():
        if config.disabled2:
            ContentType = apps.get_model("contenttypes", "ContentType")
            ct = ContentType.objects.get_for_model(config)
            OrganizationPluginConfiguration = apps.get_model(
                "api_app", "OrganizationPluginConfiguration"
            )
            for org in config.disabled2:
                if org:
                    OrganizationPluginConfiguration.objects.create(
                        organization=org,
                        object_id=config.pk,
                        content_type=ct,
                        disabled=True,
                    )


class Migration(migrations.Migration):
    dependencies = [
        ("api_app", "0056_alter_organizationpluginconfiguration_content_type"),
        ("analyzers_manager", "0058_3_change_primary_key"),
    ]

    operations = [
        migrations.RenameField(
            model_name="analyzerreport", old_name="config", new_name="old_config"
        ),
        migrations.AddField(
            model_name="analyzerreport",
            name="config",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reports",
                to="analyzers_manager.analyzerconfig",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(migrate),
        migrations.AlterUniqueTogether(
            name="analyzerreport",
            unique_together={("config", "job")},
        ),
        migrations.RemoveField(model_name="analyzerconfig", name="disabled2"),
        migrations.RemoveField(model_name="analyzerreport", name="old_config"),
    ]
