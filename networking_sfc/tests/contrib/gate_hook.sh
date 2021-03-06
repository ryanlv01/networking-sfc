#!/usr/bin/env bash

set -ex

VENV=${1:-"dsvm-functional"}

GATE_DEST=$BASE/new
NEUTRON_PATH=$GATE_DEST/networking-sfc
GATE_HOOKS=$NEUTRON_PATH/networking_sfc/tests/contrib/hooks
DEVSTACK_PATH=$GATE_DEST/devstack
LOCAL_CONF=$DEVSTACK_PATH/local.conf


# Inject config from hook into localrc
function load_rc_hook {
    local hook="$1"
    config=$(cat $GATE_HOOKS/$hook)
    export DEVSTACK_LOCAL_CONFIG+="
# generated from hook '$hook'
${config}
"
}


# Inject config from hook into local.conf
function load_conf_hook {
    local hook="$1"
    cat $GATE_HOOKS/$hook >> $LOCAL_CONF
}


case $VENV in
"dsvm-functional"|"dsvm-fullstack")
    # The following need to be set before sourcing
    # configure_for_func_testing.
    GATE_STACK_USER=stack
    PROJECT_NAME=networking-sfc
    IS_GATE=True

    source $DEVSTACK_PATH/functions
    source $NEUTRON_PATH/devstack/lib/ovs

    if [[ "$VENV" =~ "dsvm-functional" ]] ; then
        source $NEUTRON_PATH/tools/configure_for_func_testing.sh
        configure_host_for_func_testing
    fi

    # The OVS_BRANCH variable is used by git checkout. In the case below
    # we use a commit on branch-2.5 that fixes compilation with the
    # latest ubuntu trusty kernel.
    OVS_BRANCH=v2.4.0
    remove_ovs_packages
    compile_ovs True /usr /var
    start_new_ovs

    load_conf_hook iptables_verify
    load_conf_hook ovs
    # Make the workspace owned by the stack user
    sudo chown -R $STACK_USER:$STACK_USER $BASE
    ;;

*)
    echo "Unrecognized environment $VENV".
    exit 1
esac
