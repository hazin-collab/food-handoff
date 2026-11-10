# Food Batch Handoff Design

## The problem

In this example, a supplier sends a batch of food to a retailer. The supplier records when the batch leaves, and the retailer records when it arrives. If their records disagree, the two businesses have to check their delivery notes to work out what happened.

## Proposed workflow

1. The supplier registers food batch B-104 and names the retailer who will receive it.
2. When the batch leaves, the supplier marks it as dispatched.
3. When the delivery arrives, the retailer checks the batch label and confirms receipt in the app.
4. The smart contract records receipt only if the batch was dispatched and the confirmation came from the named retailer. Both parties can then see that B-104 was received.

## Benefits and limitations

The supplier can see which batches are still awaiting confirmation. If there is a delivery dispute, both businesses can check the same record to see who marked the batch as dispatched and who confirmed receipt.

The record is only as accurate as the information people enter. If the retailer confirms the wrong batch or overlooks damaged food, the blockchain will still record that confirmation.

## How we will test the handoff

| Test | Expected result |
|---|---|
| The supplier registers batch B-104 and names the retailer. | The batch shows as Registered. |
| The named retailer tries to confirm receipt before dispatch. | The contract rejects the request. The batch stays Registered. |
| The supplier marks B-104 as dispatched. | The batch shows as Dispatched. |
| A different account tries to confirm receipt. | The contract rejects the request. The batch stays Dispatched. |
| The named retailer confirms receipt. | The batch shows as Received. |
| The named retailer tries to confirm receipt again. | The contract rejects the second confirmation. The batch stays Received. |
