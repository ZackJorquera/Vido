# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/api/billing.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import metric_pb2 as google_dot_api_dot_metric__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/api/billing.proto',
  package='google.api',
  syntax='proto3',
  serialized_options=_b('\n\016com.google.apiB\014BillingProtoP\001ZEgoogle.golang.org/genproto/googleapis/api/serviceconfig;serviceconfig\242\002\004GAPI'),
  serialized_pb=_b('\n\x18google/api/billing.proto\x12\ngoogle.api\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/metric.proto\"\x93\x01\n\x07\x42illing\x12\x45\n\x15\x63onsumer_destinations\x18\x08 \x03(\x0b\x32&.google.api.Billing.BillingDestination\x1a\x41\n\x12\x42illingDestination\x12\x1a\n\x12monitored_resource\x18\x01 \x01(\t\x12\x0f\n\x07metrics\x18\x02 \x03(\tBn\n\x0e\x63om.google.apiB\x0c\x42illingProtoP\x01ZEgoogle.golang.org/genproto/googleapis/api/serviceconfig;serviceconfig\xa2\x02\x04GAPIb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_metric__pb2.DESCRIPTOR,])




_BILLING_BILLINGDESTINATION = _descriptor.Descriptor(
  name='BillingDestination',
  full_name='google.api.Billing.BillingDestination',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='monitored_resource', full_name='google.api.Billing.BillingDestination.monitored_resource', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metrics', full_name='google.api.Billing.BillingDestination.metrics', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=178,
  serialized_end=243,
)

_BILLING = _descriptor.Descriptor(
  name='Billing',
  full_name='google.api.Billing',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='consumer_destinations', full_name='google.api.Billing.consumer_destinations', index=0,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_BILLING_BILLINGDESTINATION, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=96,
  serialized_end=243,
)

_BILLING_BILLINGDESTINATION.containing_type = _BILLING
_BILLING.fields_by_name['consumer_destinations'].message_type = _BILLING_BILLINGDESTINATION
DESCRIPTOR.message_types_by_name['Billing'] = _BILLING
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Billing = _reflection.GeneratedProtocolMessageType('Billing', (_message.Message,), dict(

  BillingDestination = _reflection.GeneratedProtocolMessageType('BillingDestination', (_message.Message,), dict(
    DESCRIPTOR = _BILLING_BILLINGDESTINATION,
    __module__ = 'google.api.billing_pb2'
    # @@protoc_insertion_point(class_scope:google.api.Billing.BillingDestination)
    ))
  ,
  DESCRIPTOR = _BILLING,
  __module__ = 'google.api.billing_pb2'
  # @@protoc_insertion_point(class_scope:google.api.Billing)
  ))
_sym_db.RegisterMessage(Billing)
_sym_db.RegisterMessage(Billing.BillingDestination)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
