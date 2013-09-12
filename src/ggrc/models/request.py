# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base

class Request(Base, db.Model):
  __tablename__ = 'requests'

  VALID_TYPES = (u'documentation', u'interview', u'population sample')
  VALID_STATES = (u'Draft', u'Requested', u'Responded', u'Amended Request', u'Updated Response', u'Accepted')
  assignee_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
  assignee = db.relationship('Person')
  request_type = deferred(db.Column(db.Enum( VALID_TYPES), nullable = False), 'Request')
  status = deferred(db.Column(db.Enum(VALID_STATES), nullable = False), 'Request')
  requested_on = deferred(db.Column(db.Date, nullable=False), 'Request')
  due_on = deferred(db.Column(db.Date, nullable=False), 'Request')
  audit_id = db.Column(db.Integer, db.ForeignKey('audits.id'), nullable=False)
  objective_id = db.Column(db.Integer, db.ForeignKey('objectives.id'), nullable=False)
  gdrive_upload_path = deferred(db.Column(db.String, nullable=True), 'Request')

  #responses = db.relationship('Response', backref='request', cascade='all, delete-orphan')

  _publish_attrs = [
      'assignee',
      'request_type',
      'gdrive_upload_path',
      'requested_on',
      'due_on',
      'status',
      'audit',
      'objective',
#      'responses',
  ]
  _sanitize_html = [
      'gdrive_upload_path',
  ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Request, cls).eager_query()
    return query.options(
        orm.joinedload('audit'),
        orm.joinedload('objective'))
        #orm.subqueryload('responses'))
