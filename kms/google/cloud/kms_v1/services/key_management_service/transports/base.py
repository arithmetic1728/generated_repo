# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import abc
import typing

from google import auth
from google.auth import credentials  # type: ignore

from google.cloud.kms_v1.types import resources
from google.cloud.kms_v1.types import service


class KeyManagementServiceTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for KeyManagementService."""

    AUTH_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/cloudkms',
    )

    def __init__(
            self, *,
            host: str = 'cloudkms.googleapis.com',
            credentials: credentials.Credentials = None,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ':' not in host:
            host += ':443'
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

    @property
    def list_key_rings(self) -> typing.Callable[
            [service.ListKeyRingsRequest],
            service.ListKeyRingsResponse]:
        raise NotImplementedError

    @property
    def list_crypto_keys(self) -> typing.Callable[
            [service.ListCryptoKeysRequest],
            service.ListCryptoKeysResponse]:
        raise NotImplementedError

    @property
    def list_crypto_key_versions(self) -> typing.Callable[
            [service.ListCryptoKeyVersionsRequest],
            service.ListCryptoKeyVersionsResponse]:
        raise NotImplementedError

    @property
    def list_import_jobs(self) -> typing.Callable[
            [service.ListImportJobsRequest],
            service.ListImportJobsResponse]:
        raise NotImplementedError

    @property
    def get_key_ring(self) -> typing.Callable[
            [service.GetKeyRingRequest],
            resources.KeyRing]:
        raise NotImplementedError

    @property
    def get_crypto_key(self) -> typing.Callable[
            [service.GetCryptoKeyRequest],
            resources.CryptoKey]:
        raise NotImplementedError

    @property
    def get_crypto_key_version(self) -> typing.Callable[
            [service.GetCryptoKeyVersionRequest],
            resources.CryptoKeyVersion]:
        raise NotImplementedError

    @property
    def get_public_key(self) -> typing.Callable[
            [service.GetPublicKeyRequest],
            resources.PublicKey]:
        raise NotImplementedError

    @property
    def get_import_job(self) -> typing.Callable[
            [service.GetImportJobRequest],
            resources.ImportJob]:
        raise NotImplementedError

    @property
    def create_key_ring(self) -> typing.Callable[
            [service.CreateKeyRingRequest],
            resources.KeyRing]:
        raise NotImplementedError

    @property
    def create_crypto_key(self) -> typing.Callable[
            [service.CreateCryptoKeyRequest],
            resources.CryptoKey]:
        raise NotImplementedError

    @property
    def create_crypto_key_version(self) -> typing.Callable[
            [service.CreateCryptoKeyVersionRequest],
            resources.CryptoKeyVersion]:
        raise NotImplementedError

    @property
    def import_crypto_key_version(self) -> typing.Callable[
            [service.ImportCryptoKeyVersionRequest],
            resources.CryptoKeyVersion]:
        raise NotImplementedError

    @property
    def create_import_job(self) -> typing.Callable[
            [service.CreateImportJobRequest],
            resources.ImportJob]:
        raise NotImplementedError

    @property
    def update_crypto_key(self) -> typing.Callable[
            [service.UpdateCryptoKeyRequest],
            resources.CryptoKey]:
        raise NotImplementedError

    @property
    def update_crypto_key_version(self) -> typing.Callable[
            [service.UpdateCryptoKeyVersionRequest],
            resources.CryptoKeyVersion]:
        raise NotImplementedError

    @property
    def encrypt(self) -> typing.Callable[
            [service.EncryptRequest],
            service.EncryptResponse]:
        raise NotImplementedError

    @property
    def decrypt(self) -> typing.Callable[
            [service.DecryptRequest],
            service.DecryptResponse]:
        raise NotImplementedError

    @property
    def asymmetric_sign(self) -> typing.Callable[
            [service.AsymmetricSignRequest],
            service.AsymmetricSignResponse]:
        raise NotImplementedError

    @property
    def asymmetric_decrypt(self) -> typing.Callable[
            [service.AsymmetricDecryptRequest],
            service.AsymmetricDecryptResponse]:
        raise NotImplementedError

    @property
    def update_crypto_key_primary_version(self) -> typing.Callable[
            [service.UpdateCryptoKeyPrimaryVersionRequest],
            resources.CryptoKey]:
        raise NotImplementedError

    @property
    def destroy_crypto_key_version(self) -> typing.Callable[
            [service.DestroyCryptoKeyVersionRequest],
            resources.CryptoKeyVersion]:
        raise NotImplementedError

    @property
    def restore_crypto_key_version(self) -> typing.Callable[
            [service.RestoreCryptoKeyVersionRequest],
            resources.CryptoKeyVersion]:
        raise NotImplementedError


__all__ = (
    'KeyManagementServiceTransport',
)
