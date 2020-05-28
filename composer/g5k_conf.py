from enoslib.api import run_command, wait_ssh
from enoslib.infra.enos_g5k.provider import G5k
from enoslib.infra.enos_g5k.configuration import Configuration, NetworkConfiguration

import logging
import os


logging.basicConfig(level=logging.INFO)


network_rennes = NetworkConfiguration(
    id="n1",
    type="prod",
    roles=["my_network"],
    site="rennes"
)

network_sophia = NetworkConfiguration(
    id="n2",
    type="prod",
    roles=["my_network"],
    site="sophia"
)

network_luxembourg = NetworkConfiguration(
    id="n3",
    type="prod",
    roles=["my_network"],
    site="luxembourg"
)

network_nantes = NetworkConfiguration(
    id="n4",
    type="prod",
    roles=["my_network"],
    site="nantes"
)

network_grenoble = NetworkConfiguration(
    id="n5",
    type="prod",
    roles=["my_network"],
    site="grenoble"
)

network_nancy = NetworkConfiguration(
    id="n6",
    type="prod",
    roles=["my_network"],
    site="nancy"
)

network_lyon = NetworkConfiguration(
    id="n7",
    type="prod",
    roles=["my_network"],
    site="lyon"
)

network_lille = NetworkConfiguration(
    id="n8",
    type="prod",
    roles=["my_network"],
    site="lille"
)

conf = (
    Configuration
    .from_settings(
        job_type="allow_classic_ssh",
        job_name="MTestJob",
        walltime='8:00:00'
        #env_name="/grid5000/images/debian9-x64-base-2020032721.tgz"
    )
    #.add_network_conf(network_rennes)
    #.add_network_conf(network_nantes)
    #.add_network_conf(network_sophia)
    .add_network_conf(network_luxembourg)
    #.add_network_conf(network_grenoble)
    #.add_network_conf(network_nancy)
    .add_network_conf(network_lyon)
    .add_network_conf(network_lille)
    # .add_machine(
    #     roles=["control"],
    #     cluster="parapide",
    #     nodes=1,
    #     primary_network=network_rennes
    # )
    # .add_machine(
    #     roles=["control"],
    #     cluster="econome",
    #     nodes=2,
    #     primary_network=network_nantes
    # )
    # .add_machine(
    #     roles=["control"],
    #     cluster="uvb",
    #     nodes=2,
    #     primary_network=network_sophia
    # )
    .add_machine(
        roles=["control"],
        cluster="petitprince",
        nodes=3,
        primary_network=network_luxembourg
    )
    # .add_machine(
    #     roles=["control"],
    #     cluster="dahu",
    #     nodes=2,
    #     primary_network=network_grenoble
    # )
    # .add_machine(
    #     roles=["control"],
    #     cluster="gros",
    #     nodes=2,
    #     primary_network=network_nancy
    # )
    .add_machine(
        roles=["control"],
        cluster="nova",
        #cluster="taurus",
        nodes=2,
        primary_network=network_lyon
    )
    .add_machine(
        roles=["control"],
        cluster="chiclet",
        nodes=2,
        primary_network=network_lille
    )
    .finalize()
)


provider = G5k(conf)
roles, networks = provider.init()

# install docker
run_command("apt update", roles=roles)
run_command("apt install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common", roles=roles)
run_command("curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -", roles=roles)
run_command('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"', roles=roles)
run_command("apt update && apt-cache policy docker-ce", roles=roles)
run_command("apt install -y docker-ce", roles=roles)

#install docker-compose
run_command("sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose", roles=roles)
run_command("sudo chmod +x /usr/local/bin/docker-compose", roles=roles)

#pull and run Flink Stack
run_command("rm -rf flinkG5K", roles=roles)
run_command("git clone https://github.com/jazz09/flinkG5K.git", roles=roles)
run_command("cd flinkG5K/ && docker-compose up -d", roles=roles)

print(roles)
print(networks)

#provider.destroy()