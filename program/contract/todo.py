from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program


def approval():
    # globals
    op_add_task = Bytes("create")
    op_complete_task = Bytes("complete")
    op_remove_task = Bytes("remove")

    task = Txn.application_args[1]
    add_task = Seq(
        Assert(
                And(
                    # account has opted-in
                    App.optedIn(Int(0), Int(0)),
                )
            ),
        App.localPut(Txn.sender(), task, Int(0)),
        Approve(),
    )

    complete_task = Seq(
        Assert(
                And(
                    # account has opted-in
                    App.optedIn(Int(0), Int(0)),
                    # task is not completed
                    App.localGet(Txn.sender(), task) == Int(0),
                )
            ),
        App.localPut(Txn.sender(), task, Int(1)),
        Approve(),
    )

    remove_task = Seq(
        Assert(
                And(
                    # account has opted-in
                    App.optedIn(Int(0), Int(0)),
                    # task has been completed
                    App.localGet(Txn.sender(), task) == Int(1),
                )
            ),
        App.localDel(Txn.sender(), task),
        Approve(),
    )

    return program.event(
        init=Approve(),
        opt_in=Seq(
            Approve(),
        ),
        no_op=Cond(
            [Txn.application_args[0] == op_add_task, add_task],
            [Txn.application_args[0] == op_complete_task, complete_task],
            [Txn.application_args[0] == op_remove_task, remove_task],
        ),
    )


def clear():
    return Approve()
