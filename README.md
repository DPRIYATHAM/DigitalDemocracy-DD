# Digital Democracy - DD
*Empowering the Future of Voting*

## Problem Statement
In the current landscape of democratic processes, Electronic Voting Machines (EVMs) face challenges related to political interference, lengthy voting procedures, and potential user unfamiliarity with technology. The hackathon challenge is to design a secure and efficient voting system that addresses these issues. Key objectives include mitigating political interference through robust encryption, streamlining the voting process to reduce time, creating a user-friendly interface for mobile and web applications, ensuring transparency in the voting mechanism, and integrating secure methods for voters to cast their votes through digital platforms. Evaluation criteria will focus on the effectiveness of security measures, the efficiency of the system, user experience, and overall transparency in the electoral process. The goal is to foster innovation and develop a voting system that is both secure and accessible, meeting the demands of modern democratic elections.

## Solution
Digital Democracy is a comprehensive solution aimed at revolutionizing the democratic voting process. By addressing challenges such as political interference, time-consuming procedures, and user unfamiliarity with technology, DD ensures a secure, efficient, and user-friendly voting experience. The project incorporates cutting-edge technologies, including blockchain, advanced encryption, and innovative algorithms, to enhance transparency, security, and accessibility in democratic elections.
Long Queues Can be escaped by Random time allocation
EVM Security - Ensured by a DD application - Booth Interface
People who can vote form web/app can follow the procedure, and who couldn't will be going to the booth.
Election Commission will be getting the data, from the database in the portal.

Roles in a election - Categorical wise
1. Voter
	- APP_AVL - HOME
	- APP_UNAVL - BOOTH - No Nicknames
2. Election Commision 
	Get data, encrypted way
3. Contestants
	Can lead to Political Interference
4. Supporters (negative way)
	Can damage physical security by going home to home
5. Law and Police
	Can help with Physical Security at booth and in constituency, helping in sorting the issues.
6. Attackers
	Try to modify the data damage Confidentiality, Integrity or Availability of application or data.
7. Cyber Crime and Security Team
	Constant Monitor of attacks or tampers in any constituency and managing them efficiently.

**Key Features:**
1. `Vote from Anywhere`
   - Web Application and Mobile App to cast your vote using your mobile device.
   - Access to voting booths, centralizing booths data where you can vote in your nearest booth not necessarily to vote in the same constituency.
   - Cluster Heads of each constituency take care of vote from a partiular person.
2. `Portal`
   - Roles: Election Commission of India, Voter, Booth.
   - Integrating with dapp, ensuring the data integrity.
   - Secure Web portal from attacks.
3. `Random Slot Allocation`
   - Crowd Management for Long queues - notified prior, can request for later slots in case of unavailability.
   - Load management for the server, uniform and random distribution to maintain availability in any case.
   - Diversifying the slots in the specific constituency.
        Assumption: People Stick mostly to their Constituency.
4. `Similarity Matrix`
   - Using classical Image Recognization can be a bit complex and computationally complex task, this decreases the complexity and make the application more efficient.
   - Use of Machine Learning to decide the Similarity threshold
        - Our face similarity differs from the Aadhar card, we use ML to get a average range of similarity comparing from the Voter card to the person in general
        - Calculating it from a large and diversified range of data of present picture and the one in Voter Card.
        - Categorizing it according to Gender and age group for better classification - [Algorithm](https://github.com/DPRIYATHAM/sp1r1t/blob/main/similarity_algo.py)
```python
# For Checking the image similarity - code snippet
import face_recognition

# Load images with faces
image_of_voter_card = face_recognition.load_image_file("voter_card_face.jpg")
image_of_person = face_recognition.load_image_file("person_photo.jpg")

# Find face locations and face encodings for each image
voter_card_face_locations = face_recognition.face_locations(image_of_voter_card)
person_face_locations = face_recognition.face_locations(image_of_person)

voter_card_face_encodings = face_recognition.face_encodings(image_of_voter_card, voter_card_face_locations)
person_face_encodings = face_recognition.face_encodings(image_of_person, person_face_locations)

# Calculate similarity using FaceNet embeddings
if voter_card_face_encodings and person_face_encodings:
    voter_card_encoding = voter_card_face_encodings[0]
    person_encoding = person_face_encodings[0]

    # Calculate Euclidean distance between face embeddings
    euclidean_distance = face_recognition.face_distance([voter_card_encoding], person_encoding)

    # Set a threshold for similarity
    similarity_threshold = 0.6  # Adjust as needed

    # Compare similarity and make a decision
    if euclidean_distance < similarity_threshold:
        print("Face Authentication done")
    else:
        print("Face Authentication Failure.")
else:
    print("No faces found in one or both images.")

```
5. `Portal`
   - Roles: Election Commission of India, Voter, Booth.
   - Integrating with dapp, ensuring the data integrity.
   - Secure Web portal from attacks.
6. `NickName`
   - Colour Names for unique identification
   - Giving a custom nickname for each and every party so that, even when a user is surrounded by political influence this helps in keeping whom he voted as secret.
   - Human Phsycology - they know whom they are gonna vote before, so they are gonna fix the colour before for the party and this is done in a random time before 1 week from elections
   - This would be taken care that this will be done prior to a week of elections when the candidates are fixed, and the user will be notified upto 3 times to complete this process.
   - Failed to do so, leads to termination of their online voting, and are requested to attend the Booth and vote.
   - Stored in a secured encrypted format in the database, with a dictionary mapping colour name to candidate name.
   - [Encryption Algorithm, Secure Storage](https://github.com/DPRIYATHAM/sp1r1t/blob/main/nickname.py)
7. `Blockchain - Transparency`
   - Using Hybrid blockchain technology for ensuring the transparency and higher integrity.
   - Public -  Voters, who contribute to the blockchain, produces a block - vote and stored the hash in decentralized way.
   - Here public is devided according to constituencies, so it will be easier than a decentralized public network of complete state or more.
   - Private - Election commission of India
   - Data Securly stored and tamper resistent.
   - Cluster Head for each hyperledger fabric a cluster (channel) for each of the consistuency
   - Light weight block chain, ensurinng both integrity, transparency and efficiency by decreasing the computational costs of using public block chain.
   - Blockchain can be used for validation and proof verifying that only authenticated user had casted the vote.
   - In short a centralized data at the Central Election Commission of India from multiple decentralized constituency.
   - Ensures a user votes exactly once but not more than once through smart contracts.
   - Synchronous, user can't vote from web app and again come to booth and vote.

### User
- Login
- Authentication using Voter Id,
- Security
     - (2FA OTP)
     - Face Recognization using Similarity Matrix
- Select the Candidate you want to vote (Encoded with nickname)
- Voted, auditing with block chain, and in the database.
  
### Election Commission of India
Get the data from the database
Login 
- Authentication using Secret Id,
- Security
     - (2FA OTP)
     - Facial Recognization of the Election Commission Person
Database
   - Encrypted SPII, details about voter - displaying the constituency and no.of votes per candidate.
   - Maintains confidentiality from the ECI too, making it encrypted and masking the data.
   - Robust auditing methods to make sure things are under control, maintaing the priviliges on the database.
Getting the data, this can be used for better statics, and informing/announcing the Winners.

### Booth 
Provided with physical security in the booth.
- Login
- Authentication using Voter Id,
- Security
     - (2FA OTP)
     - Face Recognization using Similarity Matrix
- Select the Candidate you want to vote (Not Encoded with nickname)
- Voted, auditing with block chain, and in the database.

### Tech Stack

**Backend Development:**
- Language: Node.js
- Framework: Express.js
- Database: Firestore (Firebase)
- RESTful API: Express.js (Node.js)

**Frontend Development:**  
- Framework: React
- Data Visualization: D3.js

**Blockchain:**  
- Ethereum
- Solidity
- Amazon Managed Blockchain
- Hyperledger Fabric

**AI and ML:**  
- TensorFlow.js
- Pytorch

**Mobile App:**  
- Flutter
- Firebase

**Hosting:**  
- Google Cloud Platform (GCP)

**Authentication:**  
- Firebase for Authentication and authorization.

**Testing:**
Jest, Jest Runner
Postman
Cypress with Electron

**Other Technologies:**  
-  Git and GitHub for version control and collaboration.
- Taiga for project management using Agile Methodology
- Obsidian

## Novelty
Here are the top 5 novelty points with brief descriptions:

1. **Random Slot Allocation:**
   - **Description:** Efficiently manages queues by randomly allocating time slots for voters.

2. **Machine Learning in Similarity Matrix:**
   - **Description:** Adapts facial recognition thresholds dynamically using machine learning techniques.

3. **NickName Privacy Feature with RSA Encryption:**
   - **Description:** Enhances voter privacy by encrypting and securely storing party nicknames.

4. **Hybrid Blockchain for Transparency and Efficiency:**
   - **Description:** Combines public and private blockchains for transparent, efficient, and secure voting.

5. **Secure Portal:**
   - **Description:** Making the election procedure digital in a secure manner.

## Security
Here are the top 5 security aspects in the "Digital Democracy" application:

1. **Facial Recognition Security:**
   - *Measure:* Implement robust facial recognition with a dynamic similarity threshold.
   - *Rationale:* Ensures secure user authentication, minimizing unauthorized access attempts.

2. **Blockchain Tamper-Resistance:**
   - *Measure:* Utilize blockchain for immutable and tamper-resistant storage of votes.
   - *Rationale:* Safeguards against data tampering, enhancing the integrity of the electoral process.

3. **RSA Encryption for Nicknames:**
   - *Measure:* Implement RSA encryption for nickname storage in the database.
   - *Rationale:* Enhances voter privacy by securing party affiliations with strong encryption.

4. **Random Slot Allocation Security:**
   - *Measure:* Employ secure randomization algorithms for slot allocation.
   - *Rationale:* Prevents manipulation, ensuring fair and secure slot distribution for voters.

5. **Hybrid Blockchain Security Model:**
   - *Measure:* Employ a hybrid blockchain for public and private data separation.
   - *Rationale:* Protects sensitive data while providing transparency and scalability in the public domain.

*Overall Security Philosophy:*
- **Multi-Factor Authentication (MFA):**
   - *Measure:* Implement MFA, including OTPs, for user and administrative logins.
   - *Rationale:* Adds an extra layer of security, minimizing the risk of unauthorized access.
 


Thank You
- Team Sp1r1t

