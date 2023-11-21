import sqlite3
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import hashlib
import getpass

# Function to securely get user input (masked password)
def get_secure_input(prompt):
    return getpass.getpass(prompt)

# Function to generate RSA key pair
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Function to encrypt data using RSA public key
def encrypt_data(data, public_key):
    cipher_text = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Use SHA256 for MGF
            algorithm=hashes.SHA256(),  # Use SHA256 for OAEP
            label=None
        )
    )
    return cipher_text

# Function to decrypt data using RSA private key
def decrypt_data(cipher_text, private_key):
    plain_text = private_key.decrypt(
        cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Use SHA256 for MGF
            algorithm=hashes.SHA256(),  # Use SHA256 for OAEP
            label=None
        )
    ).decode()
    return plain_text

# Function to create a SQLite database connection
def create_connection():
    return sqlite3.connect("encrypted_data.db")

# Function to create a table in the database
def create_table(conn):
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id BLOB,
        encrypted_user_password BLOB,
        public_key BLOB
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")

# Function to insert encrypted data into the database
def insert_data(conn, user_id, encrypted_user_password, public_key):
    sql_insert_data = """
    INSERT INTO user_data (user_id, encrypted_user_password, public_key)
    VALUES (?, ?, ?);
    """
    try:
        c = conn.cursor()
        c.execute(sql_insert_data, (user_id, encrypted_user_password, public_key))
        conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")

# Main function
def main():
    # User identification
    user_id = input("Enter your user ID: ")
    
    # Hash the user voter ID with SHA256 to generate a unique identifier
    hashed_user_id = hashlib.sha256(user_id.encode()).hexdigest()

    # Generate RSA key pair for the user
    private_key, public_key = generate_rsa_key_pair()

    # Encrypt the hashed user ID using RSA public key
    encrypted_user_id = encrypt_data(hashed_user_id, public_key)

    print("User identification successful.")

    # Get user password securely
    user_password = get_secure_input("Enter your password: ")

    # Hash the user secret (128-bit key) using SHA256 based on aadhar number, dob, and constituency
    user_secret = hashlib.sha256("aadhar"+"dob"+"constituency".encode()).hexdigest()[:32]  # 32 bytes = 256 bits

    # Use AES symmetric encryption for securely encrypting the user password
    cipher_suite = serialization.load_pem_private_key(user_secret.encode(), password=None, backend=default_backend())
    encrypted_user_password = cipher_suite.encrypt(
        user_password.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Use SHA256 for MGF
            algorithm=hashes.SHA256(),  # Use SHA256 for OAEP
            label=None
        )
    )

    print("User password encrypted successfully.")

    # Store the encrypted_user_id, encrypted_user_password, and public_key in the database
    connection = create_connection()
    create_table(connection)
    insert_data(connection, encrypted_user_id, encrypted_user_password, public_key)
    connection.close()

    print("Encrypted data stored in the database.")

if __name__ == "__main__":
    main()
