from typing import Iterable

from eth2spec.test.phase_0.block_processing import (
    test_process_attestation,
    test_process_attester_slashing,
    test_process_block_header,
    test_process_deposit,
    test_process_proposer_slashing,
    test_process_voluntary_exit,
)

from gen_base import gen_runner, gen_typing
from gen_from_tests.gen import generate_from_tests
from preset_loader import loader
from eth2spec.phase0 import spec as spec_phase0
from eth2spec.phase1 import spec as spec_phase1


def create_provider(handler_name: str, tests_src, config_name: str) -> gen_typing.TestProvider:

    def prepare_fn(configs_path: str) -> str:
        presets = loader.load_presets(configs_path, config_name)
        spec_phase0.apply_constants_preset(presets)
        spec_phase1.apply_constants_preset(presets)
        return config_name

    def cases_fn() -> Iterable[gen_typing.TestCase]:
        return generate_from_tests(
            runner_name='operations',
            handler_name=handler_name,
            src=tests_src,
            fork_name='phase0'
        )

    return gen_typing.TestProvider(prepare=prepare_fn, make_cases=cases_fn)


if __name__ == "__main__":
    gen_runner.run_generator("operations", [
        create_provider('attestation', test_process_attestation, 'minimal'),
        create_provider('attestation', test_process_attestation, 'mainnet'),
        create_provider('attester_slashing', test_process_attester_slashing, 'minimal'),
        create_provider('attester_slashing', test_process_attester_slashing, 'mainnet'),
        create_provider('block_header', test_process_block_header, 'minimal'),
        create_provider('block_header', test_process_block_header, 'mainnet'),
        create_provider('deposit', test_process_deposit, 'minimal'),
        create_provider('deposit', test_process_deposit, 'mainnet'),
        create_provider('proposer_slashing', test_process_proposer_slashing, 'minimal'),
        create_provider('proposer_slashing', test_process_proposer_slashing, 'mainnet'),
        create_provider('voluntary_exit', test_process_voluntary_exit, 'minimal'),
        create_provider('voluntary_exit', test_process_voluntary_exit, 'mainnet'),
    ])
