"""
Example of environment variables handling.
Demonstrates how to work with environment variables and .env files.
"""

from config_loader.env import EnvFactory
from examples.resources.resource_path import env_path


def main():
    # Initialize environment factory
    factory = EnvFactory()

    # Define test variables
    var_name_1 = "test_var_1"
    undefined_key = "test_undefined_key"
    text = "environment=${test_var_2}"
    text_undefined_key = "environment=${test_undefined_key}"

    # 1. Test base environment (no .env file)
    print("1. Testing base environment (no .env file):")
    base_env = factory.create(env_path=None)
    print(f"Environment elements: {len(base_env.all())}")
    print(f"Get undefined key '{var_name_1}': {str(base_env.get(var_name_1))}")
    print(f"Get default value for '{var_name_1}': {str(base_env.get(var_name_1, 'default'))}")
    print(f"Replace variables in text '{text}': {str(base_env.replace_vars(text))}")
    print(
        "Replace variables with default value in "
        f"'{text_undefined_key}': "
        f"{str(base_env.replace_vars(text_undefined_key, 'default'))}"
    )

    # 2. Test concrete environment (with .env file)
    print("\n2. Testing concrete environment (with .env file):")
    concrete_env = factory.create(env_path=env_path())
    print(f"Environment elements: {len(concrete_env.all())}")
    print(f"Get key '{var_name_1}': {str(concrete_env.get(var_name_1))}")
    print(f"Get undefined key '{undefined_key}': {str(concrete_env.get(undefined_key))}")
    print(
        f"Get default value for '{undefined_key}': "
        f"{str(concrete_env.get(undefined_key, 'default'))}"
    )
    print(f"Replace variables in text '{text}': {str(concrete_env.replace_vars(text))}")
    print(
        "Replace variables with default value in "
        f"'{text_undefined_key}': "
        f"{str(concrete_env.replace_vars(text_undefined_key, 'default'))}"
    )

    # 3. Test undefined environment (non-existent .env file)
    print("\n3. Testing undefined environment (non-existent .env file):")
    undefined_env = factory.create(env_path=".env")
    print(f"Environment elements: {len(undefined_env.all())}")
    print(f"Get undefined key '{var_name_1}': {str(undefined_env.get(var_name_1))}")
    print(f"Get default value for '{var_name_1}': {str(undefined_env.get(var_name_1, 'default'))}")
    print(f"Replace variables in text '{text}': {str(undefined_env.replace_vars(text))}")
    print(
        "Replace variables with default value in "
        f"'{text_undefined_key}': "
        f"{str(undefined_env.replace_vars(text_undefined_key, 'default'))}"
    )

    # 4. Retest base environment
    print("\n4. Retesting base environment:")
    print(f"Get undefined key '{var_name_1}': {str(base_env.get(var_name_1))}")
    print(f"Replace variables in text '{text}': {str(base_env.replace_vars(text))}")


if __name__ == "__main__":
    main()
