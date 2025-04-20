/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28",
};
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.28",
  networks: {
    ganache: {
      url: "http://127.0.0.1:8545",  // Connect to Ganache
      accounts: [
        "0xeb5c0b83d4c000917fe415ef5886c77b4170f94fd7a5c758432498d220f60f59",
        "0x6adc6f6d2967e8c8dd7ac1ddb5704a9513e2c0ec8e337bef11b5faa4732c9abe"
      ]
    }
  }
};
