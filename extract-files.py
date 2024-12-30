#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/sm6150-common',
    'hardware/qcom-caf/sm8150',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

def custom_blob_fixup(blob_name: str, blob_path: str):
    """
    Custom blob fixup logic to add 'libcrypto_shim.so' dependency.
    """
    if blob_name in ['vendor/lib64/mediadrm/libwvdrmengine.so', 'vendor/lib64/libwvhidl.so']:
        if 'libcrypto_shim.so' not in blob_path:  # Mimics `grep -q` logic
            from subprocess import run
            run([PATCHELF, '--add-needed', 'libcrypto_shim.so', blob_path], check=True)

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.hardware.fm@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
    (
        'libOmxCore',
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    ('vendor/lib64/mediadrm/libwvdrmengine.so', 'vendor/lib64/libwvhidl.so'): custom_blob_fixup,
}  # fmt: skip

module = ExtractUtilsModule(
    'sm6150-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
