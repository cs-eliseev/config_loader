from config_loader.env import EnvFactory
from examples.resources.resource_path import env_path

factory = EnvFactory()
var_name_1 = "test_var_1"
undefined_key = "test_undefined_key"
text = "environment=${test_var_2}"
text_undefined_key = "environment=${test_undefined_key}"

path = None
base_env = factory.create(env_path=path)
print(f">>>>> Init base env env wrapper! elements: {len(base_env.all())} path: {path}")
print(f"base env get undefined key '{var_name_1}' = {str(base_env.get(var_name_1))}")
print(f"base env get default key '{var_name_1}' = {str(base_env.get(var_name_1, 'default'))}")
print(f"base text: '{text}' replace: '{str(base_env.replace_vars(text))}'")
print(
    "base default value text: '{}' replace: '{}'".format(
        text_undefined_key, str(base_env.replace_vars(text_undefined_key, "default"))
    )
)

path = env_path()
concrete_env = factory.create(env_path=path)
print(f">>>>> Init concrete env env wrapper! elements: {len(concrete_env.all())} path: {path}")
print(f"concrete env get key '{var_name_1}' = {str(concrete_env.get(var_name_1))}")
print(f"concrete env get undefined key '{undefined_key}' = {str(base_env.get(undefined_key))}")
print(
    f"concrete env get default key '{undefined_key}' = "
    f"{str(concrete_env.get(undefined_key, 'default'))}"
)
print(f"concrete text: '{text}' replace: '{str(concrete_env.replace_vars(text))}'")
print(
    "concrete default value text: '{}' replace: '{}'".format(
        text_undefined_key, str(concrete_env.replace_vars(text_undefined_key, "default"))
    )
)

path = ".env"
undefined_env = factory.create(env_path=path)
print(f">>>>> Init undefined env env wrapper! elements: {len(undefined_env.all())} path: {path}")
print(f"undefined env get undefined key '{var_name_1}' = {str(undefined_env.get(var_name_1))}")
print(
    f"undefined env get default key '{var_name_1}' = "
    f"{str(undefined_env.get(var_name_1, 'default'))}"
)
print(f"undefined text: '{text}' replace: '{str(undefined_env.replace_vars(text))}'")
print(
    "undefined default value text: '{}' replace: '{}'".format(
        text_undefined_key, str(undefined_env.replace_vars(text_undefined_key, "default"))
    )
)

print(">>>>> Retest base env")
print(f"base env get undefined key '{var_name_1}' = {str(base_env.get(var_name_1))}")
print(f"base text: '{text}' replace: '{str(base_env.replace_vars(text))}'")
