# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for custom attribute definitions model."""

from sqlalchemy.exc import IntegrityError

from ggrc import db
from ggrc import models
from integration.ggrc import TestCase


class TestCAD(TestCase):
  """Tests for basic functionality of cad model."""

  def test_setting_reserved_words(self):
    """Test setting any of the existing attribute names."""

    with self.assertRaises(ValueError):
      cad = models.CustomAttributeDefinition()
      cad.definition_type = "Section"
      cad.title = "title"

    with self.assertRaises(ValueError):
      cad = models.CustomAttributeDefinition()
      cad.title = "title"
      cad.definition_type = "Section"

    with self.assertRaises(ValueError):
      models.CustomAttributeDefinition(
          title="title",
          definition_type="Assessment",
      )

    with self.assertRaises(ValueError):
      models.CustomAttributeDefinition(
          title="TITLE",
          definition_type="Program",
      )

    with self.assertRaises(ValueError):
      models.CustomAttributeDefinition(
          title="Secondary CONTACT",
          definition_type="Program",
      )

    cad = models.CustomAttributeDefinition(
        title="non existing title",
        definition_type="Program",
    )
    self.assertEqual(cad.title, "non existing title")

  def test_setting_global_cad_names(self):
    """Test duplicates with global attribute names."""

    db.session.add(models.CustomAttributeDefinition(
        title="global cad",
        definition_type="Section",
        attribute_type="Text",
    ))
    db.session.add(models.CustomAttributeDefinition(
        title="non existing title",
        definition_type="Section",
        definition_id=1,
        attribute_type="Text",
    ))
    db.session.add(models.CustomAttributeDefinition(
        title="non existing title",
        definition_type="Section",
        definition_id=2,
        attribute_type="Text",
    ))
    db.session.commit()

    with self.assertRaises(IntegrityError):
      db.session.add(models.CustomAttributeDefinition(
          title="non existing title",
          definition_type="Section",
          definition_id=2,
          attribute_type="Text",
      ))
      db.session.commit()
    db.session.rollback()

    with self.assertRaises(ValueError):
      db.session.add(models.CustomAttributeDefinition(
          title="global cad",
          definition_type="Section",
          definition_id=2,
          attribute_type="Text",
      ))
      db.session.commit()

  def test_different_models(self):
    """Test unique names over on different models."""
    db.session.add(models.CustomAttributeDefinition(
        title="my custom attribute title",
        definition_type="Section",
        attribute_type="Text",
    ))
    db.session.commit()
    cad = models.CustomAttributeDefinition(
        title="my custom attribute title",
        definition_type="Program",
        attribute_type="Text",
    )
    self.assertEqual(cad.title, "my custom attribute title")
