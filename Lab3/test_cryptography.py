#!/usr/bin/env python3
"""
Test script for cryptography package (Fernet).
"""

import sys


def print_version():
    try:
        import cryptography
        ver = getattr(cryptography, '__version__', None)
        if not ver:
            try:
                from importlib.metadata import version as pkg_version
            except Exception:
                pkg_version = None
            if pkg_version:
                try:
                    ver = pkg_version('cryptography')
                except Exception:
                    ver = 'unknown'
        print(f'cryptography version: {ver}')
    except Exception as e:
        print('cryptography import failed:', e)
        sys.exit(1)


def test_fernet():
    try:
        from cryptography.fernet import Fernet
    except Exception as e:
        print('Failed to import Fernet:', e)
        sys.exit(1)
    key = Fernet.generate_key()
    f = Fernet(key)
    message = b'Hello from test_cryptography'
    token = f.encrypt(message)
    decrypted = f.decrypt(token)
    print('Original:', message)
    print('Encrypted token:', token)
    print('Decrypted:', decrypted)
    print('FERNET OK' if decrypted == message else 'FERNET MISMATCH')


if __name__ == '__main__':
    print_version()
    test_fernet()
    print('Test completed.')
