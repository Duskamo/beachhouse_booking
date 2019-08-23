
DROP TABLE ContactInfo;
CREATE TABLE  ContactInfo (
    contact_info_id INT AUTO_INCREMENT,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    PRIMARY KEY (contact_info_id)
);

DROP TABLE TermsConditions;
CREATE TABLE  TermsConditions (
    terms_conditions_id INT AUTO_INCREMENT,
    accepted VARCHAR(255) NOT NULL,
    PRIMARY KEY (terms_conditions_id)
);

DROP TABLE PaymentInfo;
CREATE TABLE  PaymentInfo (
    payment_info_id INT AUTO_INCREMENT,
    firstNameOnCard VARCHAR(255) NOT NULL,
    lastNameOnCard VARCHAR(255) NOT NULL,
    paymentAmount VARCHAR(255) NOT NULL,
    receiptEmail VARCHAR(255) NOT NULL,
    PRIMARY KEY (payment_info_id)
);

DROP TABLE BillingInfo;
CREATE TABLE  BillingInfo (
    billing_info_id INT AUTO_INCREMENT,
    street VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    zip VARCHAR(255) NOT NULL,
    PRIMARY KEY (billing_info_id)
);
