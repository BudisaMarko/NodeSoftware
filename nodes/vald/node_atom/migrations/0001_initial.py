# Generated by Django 3.1 on 2020-08-11 13:44

from django.db import migrations, models
import django.db.models.deletion
import node_common.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('node_common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('energy', models.DecimalField(db_index=True, decimal_places=4, max_digits=15, null=True)),
                ('lande', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('term_desc', models.CharField(max_length=86, null=True)),
                ('energy_ref_id', node_common.models.RefCharField(max_length=7, null=True)),
                ('lande_ref_id', node_common.models.RefCharField(max_length=7, null=True)),
                ('level_ref_id', node_common.models.RefCharField(max_length=7, null=True)),
                ('j', models.DecimalField(db_column='J', decimal_places=1, max_digits=3, null=True)),
                ('l', models.PositiveSmallIntegerField(db_column='L', null=True)),
                ('s', models.DecimalField(db_column='S', decimal_places=1, max_digits=3, null=True)),
                ('p', models.DecimalField(db_column='P', decimal_places=1, max_digits=3, null=True)),
                ('j1', models.DecimalField(db_column='J1', decimal_places=1, max_digits=3, null=True)),
                ('j2', models.DecimalField(db_column='J2', decimal_places=1, max_digits=3, null=True)),
                ('k', models.DecimalField(db_column='K', decimal_places=1, max_digits=3, null=True)),
                ('s2', models.DecimalField(db_column='S2', decimal_places=1, max_digits=3, null=True)),
                ('jc', models.DecimalField(db_column='Jc', decimal_places=1, max_digits=3, null=True)),
                ('sn', models.PositiveSmallIntegerField(db_column='Sn', null=True)),
                ('n', models.PositiveSmallIntegerField(db_column='n', null=True)),
                ('species', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.DO_NOTHING, to='node_common.species')),
            ],
            options={
                'db_table': 'states',
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('wave', models.DecimalField(db_index=True, decimal_places=8, max_digits=16)),
                ('waveritz', models.DecimalField(db_index=True, decimal_places=8, max_digits=16)),
                ('loggf', models.DecimalField(decimal_places=3, max_digits=8, null=True)),
                ('einsteina', models.DecimalField(db_index=True, decimal_places=3, max_digits=20, null=True)),
                ('gammarad', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('gammastark', models.DecimalField(decimal_places=3, max_digits=7, null=True)),
                ('gammawaals', models.DecimalField(decimal_places=3, max_digits=6, null=True)),
                ('sigmawaals', models.PositiveSmallIntegerField(null=True)),
                ('alphawaals', models.DecimalField(decimal_places=3, max_digits=6, null=True)),
                ('accurflag', models.CharField(max_length=1, null=True)),
                ('accur', models.DecimalField(decimal_places=3, max_digits=6, null=True)),
                ('wave_ref_id', node_common.models.RefCharField(max_length=7, null=True)),
                ('waveritz_ref_id', node_common.models.RefCharField(max_length=7, null=True)),
                ('loggf_ref_id', node_common.models.RefCharField(max_length=7, null=True)),
                ('gammarad_ref_id', node_common.models.RefCharField(max_length=7, null=True)),
                ('gammastark_ref_id', node_common.models.RefCharField(max_length=7, null=True)),
                ('waals_ref_id', node_common.models.RefCharField(max_length=7, null=True)),
                ('transition_type', models.CharField(max_length=2, null=True)),
                ('autoionized', models.BooleanField(default=False, null=True)),
                ('method_return', models.PositiveSmallIntegerField(null=True)),
                ('method_restrict', models.PositiveSmallIntegerField(db_index=True, null=True)),
                ('lostate', models.ForeignKey(db_column='lostate', db_index=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='islowerstate_trans', to='node_atom.state')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='node_common.species')),
                ('upstate', models.ForeignKey(db_column='upstate', db_index=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='isupperstate_trans', to='node_atom.state')),
                ('wave_linelist', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='iswavelinelist_trans', to='node_common.linelist')),
            ],
            options={
                'db_table': 'transitions',
            },
        ),
    ]
