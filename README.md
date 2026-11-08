Food Handoff

Distributed Digital Transactions · CA1

Project proposal

A supplier dispatches a food batch to a named retailer. Today the two parties may keep separate dispatch and intake records. When they disagree about a delivery, each must consult the other. This prototype will let both parties inspect the same handoff history.

Demonstration

The supplier registers a sample batch and names the retailer's Ethereum address.

The supplier records dispatch. The retailer can inspect the batch and its status.

Only the named retailer can confirm receipt of a dispatched batch. The contract records the change and emits an event.

A third account attempts to confirm receipt. The transaction must fail and leave the batch unchanged. A second confirmation by the retailer must also fail.

Use fictitious batch identifiers. Keep delivery documents off-chain. The record shows which account acknowledged receipt. It cannot independently establish a batch's physical condition.

Planned implementation

Use Solidity and Remix IDE for the contract, Gaache for a local blockchain, Python for the two-party demonstration, and a shell script to run the demo. Preserve screenshots of the real deployment and checks for the poster and video.

Status

Initial scope. Implementation and verification are upcoming.
