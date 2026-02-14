-- Healthcare Database Schema
-- Table: patients

CREATE TABLE `patients` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `blood_type` varchar(5) DEFAULT NULL,
  `medical_condition` varchar(50) DEFAULT NULL,
  `date_of_admission` date DEFAULT NULL,
  `doctor` varchar(100) DEFAULT NULL,
  `hospital` varchar(100) DEFAULT NULL,
  `insurance_provider` varchar(50) DEFAULT NULL,
  `billing_amount` decimal(10,2) DEFAULT NULL,
  `room_number` int DEFAULT NULL,
  `admission_type` varchar(50) DEFAULT NULL,
  `discharge_date` date DEFAULT NULL,
  `medication` varchar(100) DEFAULT NULL,
  `test_results` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=55501 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;