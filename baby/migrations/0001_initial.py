# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Baby'
        db.create_table('baby_baby', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=40, null=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True)),
            ('sex', self.gf('django.db.models.fields.TextField')(max_length=10, null=True)),
            ('weight', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('height', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('homeaddr', self.gf('django.db.models.fields.TextField')(max_length=100, null=True)),
            ('schooladdr', self.gf('django.db.models.fields.TextField')(max_length=100, null=True)),
            ('homepoint', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
        ))
        db.send_create_signal('baby', ['Baby'])


    def backwards(self, orm):
        # Deleting model 'Baby'
        db.delete_table('baby_baby')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'baby.baby': {
            'Meta': {'object_name': 'Baby'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'height': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'homeaddr': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True'}),
            'homepoint': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '40', 'null': 'True'}),
            'schooladdr': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True'}),
            'sex': ('django.db.models.fields.TextField', [], {'max_length': '10', 'null': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['baby']