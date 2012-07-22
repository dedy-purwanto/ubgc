# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Entry'
        db.create_table('entries_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('embed_code', self.gf('django.db.models.fields.TextField')()),
            ('tags', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('entries', ['Entry'])


    def backwards(self, orm):
        # Deleting model 'Entry'
        db.delete_table('entries_entry')


    models = {
        'entries.entry': {
            'Meta': {'object_name': 'Entry'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'embed_code': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['entries']