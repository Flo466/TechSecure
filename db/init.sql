-- 1. Create database if it does not exist
CREATE DATABASE IF NOT EXISTS techsecure_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE techsecure_db;

-- 2. Subsidiaries table (Centralized data from Paris, Lyon, and Marseille offices)
CREATE TABLE IF NOT EXISTS filiales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ville VARCHAR(100) NOT NULL,
    adresse VARCHAR(255) NOT NULL,
    responsable VARCHAR(100) NOT NULL,
    employes INT NOT NULL,
    ip_reseau VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- 3. Contact requests table (Website contact form submissions)
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 4. Seed initial branch data
INSERT INTO filiales (ville, adresse, responsable, employes, ip_reseau) VALUES
('Paris', '102 Avenue de la République, 75011 Paris', 'Jean Dupont', 80, '10.10.1.0/24'),
('Lyon', '15 Rue de la Bannière, 69003 Lyon', 'Sophie Martin', 45, '10.20.1.0/24'),
('Marseille', '45 Boulevard du Prado, 13006 Marseille', 'Marc Bouvier', 30, '10.30.1.0/24')
ON DUPLICATE KEY UPDATE ville=ville; -- Prevent duplicates if container restarts

-- 5. Enforce least privilege principle for the application user
-- Restrict techuser permissions to strict app requirements (no DROP permissions)
GRANT SELECT, INSERT ON techsecure_db.* TO 'techuser'@'%';
FLUSH PRIVILEGES;