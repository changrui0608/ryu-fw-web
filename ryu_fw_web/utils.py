def flatten_rules(rules):
    """
    convert rules from api to a flat list
    """
    rtn = []
    for switch in rules:
        switch_id = switch['switch_id']
        for ac_list in switch['access_control_list']:
            for rule in ac_list['rules']:
                rule['switch_id'] = switch_id
                rtn.append(rule)
    return rtn


def is_pure_ip_rule(rule):
    if set(['in_port', 'dl_src', 'dl_dst', 'nw_proto']) & set(rule.keys()):
        return False
    if not set(['nw_src', 'nw_dst', 'ipv6_src', 'ipv6_src']) & set(rule.keys()):
        return False
    return True


def filter_pure_ip_rules(rules):
    """
    filter out the pure IP rules
    """
    return filter(is_pure_ip_rule, rules)


def is_global_rule(rule):
    """
    rules that have field: dl_type
    do NOT have field: nw_src nw_dst ipv6_src ipv6_dst nw_proto tp_src tp_dst
    """
    unset = set(['nw_src', 'nw_dst', 'ipv6_src', 'ipv6_dst', 'nw_proto', 'tp_src', 'tp_dst'])
    if unset & set(rule.keys()):
        return False
    return True


def filter_global_rules(rules):
    return filter(is_global_rule, rules)
