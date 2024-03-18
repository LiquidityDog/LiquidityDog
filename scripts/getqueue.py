queue = Contract.from_abi("queue", "0x725dfaf0E481653Ab86b2B071027e5DAA05cE8b4", [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "dequeue",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "holder",
						"type": "address"
					},
					{
						"internalType": "int256",
						"name": "amount",
						"type": "int256"
					},
					{
						"internalType": "uint256",
						"name": "rewardDate",
						"type": "uint256"
					}
				],
				"internalType": "struct Structures.Share",
				"name": "data",
				"type": "tuple"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "holder",
						"type": "address"
					},
					{
						"internalType": "int256",
						"name": "amount",
						"type": "int256"
					},
					{
						"internalType": "uint256",
						"name": "rewardDate",
						"type": "uint256"
					}
				],
				"internalType": "struct Structures.Share",
				"name": "data",
				"type": "tuple"
			}
		],
		"name": "enqueue",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getFirst",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "holder",
						"type": "address"
					},
					{
						"internalType": "int256",
						"name": "amount",
						"type": "int256"
					},
					{
						"internalType": "uint256",
						"name": "rewardDate",
						"type": "uint256"
					}
				],
				"internalType": "struct Structures.Share",
				"name": "data",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "isEmpty",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
])