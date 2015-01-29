#!/usr/bin/python
from ConfigParser import RawConfigParser
from onappapi import OnApp
import os, sys, argparse, json

def get_arg(resource = None):
    if len(sys.argv) > 0: return sys.argv.pop(0)
    else: usage(resource)

cmd = get_arg()

def usage(resource = None):
    if resource:
        if resource == 'vm':
            print '%s vm action' % cmd
            print 'Available actions: list, info, start, stop, shutdown, delete'
            print 'Example:'
            print '\t%s shutdown 45' % cmd
            print '\t%s start 45' % cmd
        elif resource == 'template':
            print '%s template action' % cmd
            print 'Available actions: list'
        elif resource == 'cache':
            print '%s cache clear' % cmd
    else:
        print '%s resource action' % cmd
        print 'Available resources: vm, template, cache'

    sys.exit(0)

conf = os.path.join(os.path.expanduser("~"), '.pyonapp.conf')
config = RawConfigParser()

if not os.path.exists(conf):
    config.add_section('onapp')
    config.set('onapp', 'user', raw_input('Username: '))
    config.set('onapp', 'password', raw_input('Passowrd: '))
    config.set('onapp', 'url', raw_input('Hostname: '))
    with open(conf, 'wb') as openconf: config.write(openconf)
else: config.read(conf)

user = config.get('onapp', 'user')
password = config.get('onapp', 'password')
url = config.get('onapp', 'url')

api = OnApp(user, password, url)

resource = get_arg()
if resource: action = get_arg(resource)

if resource == 'vm':
    if  action == 'list':
        api.vm_list()
    elif action == 'info':
        vm_id = get_arg(resource)
        api.vm_info(vm_id)
    elif action == 'browser':
        vm_id = get_arg(resource)
        api.vm_browser(vm_id)
    elif action == 'start':
        vm_id = get_arg(resource)
        api.vm_start(vm_id)
    elif action == 'stop':
        vm_id = get_arg(resource)
        api.vm_stop(vm_id)
    elif action == 'shutdown':
        vm_id = get_arg(resource)
        api.vm_shutdown(vm_id)
    elif action == 'delete':
        vm_id = get_arg(resource)
        api.vm_delete(vm_id)
    elif action == 'create':
        parser = argparse.ArgumentParser(prog='onappcli vm create')
        parser.add_argument('--memory', help='Max Memory', dest='memory', required = True, type = int)
        parser.add_argument('--cpus', help='Max CPU', dest='cpus', required = True, type = int)
        parser.add_argument('--cpu_shares', help='CPU Shares', dest='cpu_shares', default = 100, type = int)
        parser.add_argument('--cpu-sockets', help='CPU Sockets', dest='cpu_sockets', default = 1, type = int)
        parser.add_argument('--cpu-threads', help='CPU Threads', dest='cpu_threads', default = 1, type = int)
        parser.add_argument('--hostname', help='Set hostname', dest='hostname', required = True, type = str)
        parser.add_argument('--label', help='Set label', dest='label', required = True, type = str)
        parser.add_argument('--data-store-group-primary-id', help='Primary Datastore ID', required = True, type = int)
        parser.add_argument('--primary-disk-size', help='Set primary disk size', dest='primary_disk_size', default = 5, type = int)
        parser.add_argument('--primary-disk-min-iops', help='Primary disk IOPS', dest='primary_disk_min_iops', default = 100, type = int)
        parser.add_argument('--data-store-group-swap-id', help='Swap Datastore ID', default = 1, type = int)
        parser.add_argument('--swap-disk-size', help='Set swap disk size', dest='swap_disk_size', default = 0, type = int)
        parser.add_argument('--swap-disk-min-iops', help='Swap disk IOPS', dest='swap_disk_min_iops', default = 100, type = int)
        parser.add_argument('--primary-network-group-id', help='Network zone', dest='primary_network_group_id', required = True, type = int)
        parser.add_argument('--primary-network-id', help='Set primary network id', dest='primary_network_id', required = True, type = int)
        parser.add_argument('--selected-ip-address-id', help='Primary IP address ID', dest='selected_ip_address_id', default = 0, type = int)
        parser.add_argument('--required-virtual-machine-build', help='Build virtual machine', dest='required_virtual_machine_build', default=1, type = int)
        parser.add_argument('--required-virtual-machine-startup', help='Start after create', dest='required_virtual_machine_startup', default = 1, type = int)
        parser.add_argument('--required-ip-address-assignment', help='Auto assing IP', dest='required_ip_address_assignment', default = 1, type = int)
        parser.add_argument('--required-automatic-backup', help='Auto backups', dest='required_automatic_backup', default = 0, type = int)
        parser.add_argument('--type-of-format', help='Type of disk format', dest='type_of_format', default = 'ext4', type = str)
        parser.add_argument('--enable-autoscale', help='Enable autoscale', dest='enable_autoscale', default = 0, type = int)
        parser.add_argument('--recipe-ids', help='Recipe IDs', dest='recipe_ids', default = [], type = list)
        parser.add_argument('--custom-recipe-variables', help='Custom recipe variables', default = [], type = list)
        parser.add_argument('--template-id', help='Template ID', dest='template_id', required = True, type = int)
        parser.add_argument('--initial-root-password', help='Root password', dest='initial_root_password', required = True, type = str)
        parser.add_argument('--rate-limit', help='Rate limit', dest='rate_limit', default = 'none', type = str)
        parser.add_argument('--hypervisor-group-id', help='Hypervisor group id', dest='hypervisor_group_id', type = int)
        parser.add_argument('--hypervisor-id', help='Hypervisor', dest='hypervisor_id', required = True, type = int)
        parser.add_argument('--licensing-server-id', help='Licensing server', dest='licensing_server_id', default = 0, type = int)
        parser.add_argument('--licensing-type', help='License type', dest='licensing_type', default = 'kms', type = str)
        parser.add_argument('--licensing-key', help='License Key', dest='licensing_key', default = '', type = str)

        args = vars(parser.parse_args([] if len(sys.argv) == 0 else sys.argv))
        api.vm_create(**args)
    else: usage('vm')

elif resource == 'template':
    if action == 'list':
        api.template_list()
    else: usage('template')
elif resource == 'cache':
    if action == 'clear':
        api.clear_cache()
    else: usage('cache')
else: usage()
