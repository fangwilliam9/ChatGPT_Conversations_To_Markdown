## Will:

 # =========================
# 5. 计算 FLOPs（计算量）
# =========================
def get_flops(model):
    concrete_func = tf.function(lambda x: model(x))
    concrete_func = concrete_func.get_concrete_function(
        tf.TensorSpec([1, 224, 224, 3], tf.float32)
    )
    frozen_func, _ = tf.compat.v1.graph_util.convert_variables_to_constants_v2_as_graph(
        concrete_func.graph
    )
    flops = tf.profiler.experimental.ProfileOptionBuilder.float_operation()
    return tf.profiler.profile(frozen_func, options=flops).total_float_ops

flops = get_flops(model) / 1e9  # 转换为 GFLOPs
print(f"\n=== 计算量 (FLOPs) ===")
print(f"Model FLOPs: {flops:.2f} GFLOPs")

为什么报错：
AttributeError: module 'tensorflow._api.v2.compat.v1.graph_util' has no attribute 'convert_variables_to_constants_v2_as_graph'

## ChatGPT:

 你的错误是因为 `tensorflow._api.v2.compat.v1.graph_util` 没有 `convert_variables_to_constants_v2_as_graph` 这个属性。  

## **解决方案**
### 1. **使用 `tf.compat.v1.graph_util.convert_variables_to_constants`**
在 TensorFlow 2.x 中，如果使用 `tf.compat.v1`，应该用 `convert_variables_to_constants` 而不是 `convert_variables_to_constants_v2_as_graph`，例如：
```python
import tensorflow as tf

def get_flops(model):
    concrete_func = tf.function(lambda x: model(x))
    concrete_func = concrete_func.get_concrete_function(
        tf.TensorSpec([1, 224, 224, 3], tf.float32)
    )

    # 获取计算图
    frozen_func = tf.compat.v1.graph_util.convert_variables_to_constants(
        sess=tf.compat.v1.Session(),
        input_graph_def=concrete_func.graph.as_graph_def(),
        output_node_names=[node.op.name for node in concrete_func.graph.as_graph_def().node]
    )

    # 计算 FLOPs
    flops = tf.profiler.experimental.ProfileOptionBuilder.float_operation()
    return tf.profiler.profile(frozen_func, options=flops).total_float_ops

# 假设你有一个 TensorFlow Keras 模型
model = tf.keras.applications.MobileNetV2(weights=None, input_shape=(224, 224, 3))

flops = get_flops(model) / 1e9  # 转换为 GFLOPs
print(f"\n=== 计算量 (FLOPs) ===")
print(f"Model FLOPs: {flops:.2f} GFLOPs")
```
但 `tf.compat.v1.Session()` 在 TensorFlow 2.x 可能需要运行在 `tf.compat.v1.disable_eager_execution()` 模式下，否则会有 `RuntimeError`。

---

### 2. **使用 `convert_to_constants`（更推荐）**
如果你想用 TensorFlow 2.x 的方法，可以改用 `tf.keras.models.save_model` + `convert_to_constants`：
```python
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2
import tensorflow as tf

def get_flops(model):
    concrete_func = tf.function(lambda x: model(x))
    concrete_func = concrete_func.get_concrete_function(
        tf.TensorSpec([1, 224, 224, 3], tf.float32)
    )

    frozen_func = convert_variables_to_constants_v2(concrete_func)
    frozen_graph = frozen_func.graph

    flops = tf.profiler.experimental.ProfileOptionBuilder.float_operation()
    return tf.profiler.profile(frozen_graph, options=flops).total_float_ops

model = tf.keras.applications.MobileNetV2(weights=None, input_shape=(224, 224, 3))

flops = get_flops(model) / 1e9  # 转换为 GFLOPs
print(f"\n=== 计算量 (FLOPs) ===")
print(f"Model FLOPs: {flops:.2f} GFLOPs")
```
这个方法适用于 TensorFlow 2.x，并避免了 `compat.v1` 相关的问题。

---

### **总结**
- **如果你用的是 TensorFlow 1.x 兼容模式**，用 `convert_variables_to_constants` 并在 `tf.compat.v1.disable_eager_execution()` 下运行。
- **如果你用的是 TensorFlow 2.x**，推荐使用 `convert_variables_to_constants_v2`。

