# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gym_grpc/gym_rlay.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder


# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x17gym_grpc/gym_rlay.proto\x12\x03\x65nv\x1a\x1cgoogle/protobuf/struct.proto"\x17\n\x05\x45nvID\x12\x0e\n\x06\x65nv_id\x18\x01 \x01(\t"\x18\n\x06Status\x12\x0e\n\x06status\x18\x01 \x01(\x08"8\n\nNumpyArray\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x12\r\n\x05shape\x18\x02 \x01(\x0c\x12\r\n\x05\x64type\x18\x03 \x01(\t"5\n\x07NDArray\x12\r\n\x05shape\x18\x01 \x03(\x05\x12\x0c\n\x04\x64\x61ta\x18\x02 \x03(\x02\x12\r\n\x05\x64type\x18\x03 \x01(\t"\x18\n\x06\x41\x63tion\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\x05"\x14\n\x04Seed\x12\x0c\n\x04seed\x18\x01 \x01(\x05"z\n\x07Options\x12(\n\x06params\x18\x01 \x03(\x0b\x32\x18.env.Options.ParamsEntry\x1a\x45\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01"t\n\x04Info\x12%\n\x06params\x18\x01 \x03(\x0b\x32\x15.env.Info.ParamsEntry\x1a\x45\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01"\x9d\x01\n\tResetArgs\x12\x11\n\x04seed\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12,\n\x07options\x18\x02 \x03(\x0b\x32\x1b.env.ResetArgs.OptionsEntry\x1a\x46\n\x0cOptionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01\x42\x07\n\x05_seed"\xcc\x01\n\nStepReturn\x12\x19\n\x03obs\x18\x01 \x01(\x0b\x32\x0c.env.NDArray\x12\x0e\n\x06reward\x18\x02 \x01(\x02\x12\x12\n\nterminated\x18\x03 \x01(\x08\x12\x11\n\ttruncated\x18\x04 \x01(\x08\x12\'\n\x04info\x18\x05 \x03(\x0b\x32\x19.env.StepReturn.InfoEntry\x1a\x43\n\tInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01"\xc1\x01\n\x10GymnasiumMessage\x12&\n\x0bstep_return\x18\x01 \x01(\x0b\x32\x0f.env.StepReturnH\x00\x12$\n\nreset_args\x18\x03 \x01(\x0b\x32\x0e.env.ResetArgsH\x00\x12\x1e\n\x06\x61\x63tion\x18\x04 \x01(\x0b\x32\x0c.env.NDArrayH\x00\x12\x0f\n\x05\x63lose\x18\x05 \x01(\x08H\x00\x12\x11\n\x07request\x18\x06 \x01(\x08H\x00\x12\x10\n\x06status\x18\x07 \x01(\x08H\x00\x42\t\n\x07message2\x82\x01\n\x03\x45nv\x12\'\n\nInitialize\x12\n.env.EnvID\x1a\x0b.env.Status"\x00\x12*\n\x05Reset\x12\x0e.env.ResetArgs\x1a\x0f.env.StepReturn"\x00\x12&\n\x04Step\x12\x0b.env.Action\x1a\x0f.env.StepReturn"\x00\x62\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "gym_grpc.gym_rlay_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _OPTIONS_PARAMSENTRY._options = None
    _OPTIONS_PARAMSENTRY._serialized_options = b"8\001"
    _INFO_PARAMSENTRY._options = None
    _INFO_PARAMSENTRY._serialized_options = b"8\001"
    _RESETARGS_OPTIONSENTRY._options = None
    _RESETARGS_OPTIONSENTRY._serialized_options = b"8\001"
    _STEPRETURN_INFOENTRY._options = None
    _STEPRETURN_INFOENTRY._serialized_options = b"8\001"
    _ENVID._serialized_start = 62
    _ENVID._serialized_end = 85
    _STATUS._serialized_start = 87
    _STATUS._serialized_end = 111
    _NUMPYARRAY._serialized_start = 113
    _NUMPYARRAY._serialized_end = 169
    _NDARRAY._serialized_start = 171
    _NDARRAY._serialized_end = 224
    _ACTION._serialized_start = 226
    _ACTION._serialized_end = 250
    _SEED._serialized_start = 252
    _SEED._serialized_end = 272
    _OPTIONS._serialized_start = 274
    _OPTIONS._serialized_end = 396
    _OPTIONS_PARAMSENTRY._serialized_start = 327
    _OPTIONS_PARAMSENTRY._serialized_end = 396
    _INFO._serialized_start = 398
    _INFO._serialized_end = 514
    _INFO_PARAMSENTRY._serialized_start = 327
    _INFO_PARAMSENTRY._serialized_end = 396
    _RESETARGS._serialized_start = 517
    _RESETARGS._serialized_end = 674
    _RESETARGS_OPTIONSENTRY._serialized_start = 595
    _RESETARGS_OPTIONSENTRY._serialized_end = 665
    _STEPRETURN._serialized_start = 677
    _STEPRETURN._serialized_end = 881
    _STEPRETURN_INFOENTRY._serialized_start = 814
    _STEPRETURN_INFOENTRY._serialized_end = 881
    _GYMNASIUMMESSAGE._serialized_start = 884
    _GYMNASIUMMESSAGE._serialized_end = 1077
    _ENV._serialized_start = 1080
    _ENV._serialized_end = 1210
# @@protoc_insertion_point(module_scope)
