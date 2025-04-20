// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HospitalManagement {
    address public admin;
    
    enum Role { Patient, Doctor, Admin, None }
    
    struct User {
        address userAddress;
        string name;
        Role role;
        bool isApproved;
    }
    
    struct Appointment {
        uint id;
        address patient;
        address doctor;
        string details;
        bool isApprovedByDoctor;
        bool isApprovedByAdmin;
    }
    
    mapping(address => User) public users;
    mapping(uint => Appointment) public appointments;
    uint public appointmentCount;
    
    mapping(address => mapping(address => bool)) public dataAccess; // Patient grants access to doctors
    
    event UserRegistered(address indexed user, string name, Role role);
    event UserApproved(address indexed user, Role role);
    event AppointmentBooked(uint indexed id, address patient, address doctor);
    event AppointmentApproved(uint indexed id, address approver);
    event DataShared(address indexed patient, address indexed doctor, bool isGranted);
    
    modifier onlyAdmin() {
        require(users[msg.sender].role == Role.Admin, "Only admin can perform this action");
        _;
    }
    
    modifier onlyDoctor() {
        require(users[msg.sender].role == Role.Doctor, "Only doctors can perform this action");
        _;
    }
    
    modifier onlyPatient() {
        require(users[msg.sender].role == Role.Patient, "Only patients can perform this action");
        _;
    }
    
    constructor() {
        admin = msg.sender;
        users[msg.sender] = User(msg.sender, "Admin", Role.Admin, true);
    }
    
    function registerUser(string memory _name, Role _role) external {
        require(users[msg.sender].role == Role.None, "User already registered");
        require(_role == Role.Patient || _role == Role.Doctor, "Invalid role");
        users[msg.sender] = User(msg.sender, _name, _role, false);
        emit UserRegistered(msg.sender, _name, _role);
    }
    
    function approveUser(address _user) external onlyAdmin {
        require(users[_user].role != Role.None, "User not found");
        require(!users[_user].isApproved, "User already approved");
        users[_user].isApproved = true;
        emit UserApproved(_user, users[_user].role);
    }
    
    function bookAppointment(address _doctor, string memory _details) external onlyPatient {
        require(users[_doctor].role == Role.Doctor, "Invalid doctor");
        require(users[_doctor].isApproved, "Doctor not approved");
        appointmentCount++;
        appointments[appointmentCount] = Appointment(appointmentCount, msg.sender, _doctor, _details, false, false);
        emit AppointmentBooked(appointmentCount, msg.sender, _doctor);
    }
    
    function approveAppointment(uint _id) external {
        require(appointments[_id].id != 0, "Invalid appointment");
        require(msg.sender == admin || msg.sender == appointments[_id].doctor, "Not authorized");
        
        if (msg.sender == appointments[_id].doctor) {
            appointments[_id].isApprovedByDoctor = true;
        } else {
            appointments[_id].isApprovedByAdmin = true;
        }
        emit AppointmentApproved(_id, msg.sender);
    }
    
    function grantDataAccess(address _doctor) external onlyPatient {
        require(users[_doctor].role == Role.Doctor, "Invalid doctor");
        dataAccess[msg.sender][_doctor] = true;
        emit DataShared(msg.sender, _doctor, true);
    }
    
    function revokeDataAccess(address _doctor) external onlyPatient {
        require(dataAccess[msg.sender][_doctor], "Access not granted");
        dataAccess[msg.sender][_doctor] = false;
        emit DataShared(msg.sender, _doctor, false);
    }
    
    function checkDataAccess(address _patient) external view onlyDoctor returns (bool) {
        return dataAccess[_patient][msg.sender];
    }
}
