// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FoodHandoff {
    enum BatchStatus {
        Registered,
        Dispatched,
        Received
    }

    struct Batch {
        address supplier;
        address retailer;
        BatchStatus status;
    }

    mapping(string => Batch) private batches;

    event BatchRegistered(string batchId, address supplier, address retailer);

    function registerBatch(string calldata batchId, address retailer) external {
        require(bytes(batchId).length > 0, "Enter a batch ID");
        require(batches[batchId].supplier == address(0), "Batch already registered");
        require(retailer != address(0), "Enter a retailer address");
        require(retailer != msg.sender, "Supplier and retailer must be different");

        batches[batchId] = Batch({
            supplier: msg.sender,
            retailer: retailer,
            status: BatchStatus.Registered
        });

        emit BatchRegistered(batchId, msg.sender, retailer);
    }

    event BatchDispatched(string batchId, address supplier);

    function dispatchBatch(string calldata batchId) external {
        Batch storage batch = batches[batchId];

        require(batch.supplier != address(0), "Batch does not exist");
        require(msg.sender == batch.supplier, "Only the supplier can dispatch");
        require(batch.status == BatchStatus.Registered, "Batch must be registered");

        batch.status = BatchStatus.Dispatched;
        emit BatchDispatched(batchId, msg.sender);
    }

    event BatchReceived(string batchId, address retailer);

    function confirmReceipt(string calldata batchId) external {
        Batch storage batch = batches[batchId];

        require(batch.supplier != address(0), "Batch does not exist");
        require(msg.sender == batch.retailer, "Only the named retailer can confirm");
        require(batch.status == BatchStatus.Dispatched, "Batch must be dispatched");

        batch.status = BatchStatus.Received;
        emit BatchReceived(batchId, msg.sender);
    }

    function getBatch(string calldata batchId)
        external
        view
        returns (address supplier, address retailer, BatchStatus status)
    {
        Batch storage batch = batches[batchId];
        require(batch.supplier != address(0), "Batch does not exist");

        return (batch.supplier, batch.retailer, batch.status);
    }
}