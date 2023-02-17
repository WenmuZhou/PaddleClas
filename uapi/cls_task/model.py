# Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved. 
#   
# Licensed under the Apache License, Version 2.0 (the "License");   
# you may not use this file except in compliance with the License.  
# You may obtain a copy of the License at   
#   
#     http://www.apache.org/licenses/LICENSE-2.0    
#   
# Unless required by applicable law or agreed to in writing, software   
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
# See the License for the specific language governing permissions and   
# limitations under the License.

import os

from ..base import BaseModel
from ..base.utils.path import get_cache_dir
from ..base.utils.arg import CLIArgument
from ..base.utils.misc import abspath


class ClsModel(BaseModel):
    def train(self,
              dataset=None,
              batch_size=None,
              learning_rate=None,
              epochs_iters=None,
              device='gpu',
              resume_path=None,
              dy2st=False,
              amp=None,
              use_vdl=True,
              save_dir=None):
        # NOTE: We must use an absolute path here, 
        # so we can run the scripts either inside or outside the repo dir.
        if dataset is not None:
            dataset = abspath(dataset)
        if resume_path is not None:
            resume_path = abspath(resume_path)
        if save_dir is not None:
            save_dir = abspath(save_dir)
        else:
            # `save_dir` is None
            save_dir = abspath(os.path.join('output', 'train'))

        # Update YAML config file
        config = self.config.copy()
        config.update_dataset(dataset)
        config.update_amp(amp)
        config.update_device(device)

        if batch_size is not None:
            config.update_batch_size(batch_size)
        if learning_rate is not None:
            config.update_lr_scheduler(learning_rate)
        if epochs_iters is not None:
            config.update([f'Global.epochs={epochs_iters}'])
        if resume_path is not None:
            config.update(
                [f'Global.checkpoints={resume_path.replace(".pdparams","")}'])
        if dy2st:
            config.update([f'Global.to_static={True}'])
        if use_vdl:
            config.update([f'Global.use_visualdl={use_vdl}'])
        if save_dir is not None:
            config.update([f'Global.output_dir={save_dir}'])
        config_path = self._config_path
        config.dump(config_path)
        self.runner.train(config_path, [], device)

    def predict(self, weight_path, input_path, device='gpu', save_dir=None):
        weight_path = abspath(weight_path)
        input_path = abspath(input_path)
        if save_dir is not None:
            save_dir = abspath(save_dir)
        else:
            # `save_dir` is None
            save_dir = abspath(os.path.join('output', 'predict'))

        # Update YAML config file
        config = self.config.copy()
        if weight_path is not None:
            config.update([
                f'Global.pretrained_model={weight_path.replace(".pdparams","")}'
            ])
        if input_path is not None:
            config.update([f'Infer.infer_imgs={input_path}'])
        if save_dir is not None:
            pass
        config_path = self._config_path
        config.dump(config_path)

        self.runner.predict(config_path, [], device)

    def export(self, weight_path, save_dir=None, input_shape=None):
        weight_path = abspath(weight_path)
        if save_dir is not None:
            save_dir = abspath(save_dir)
        else:
            # `save_dir` is None
            save_dir = abspath(os.path.join('output', 'export'))

        # Update YAML config file
        config = self.config.copy()
        if weight_path is not None:
            config.update([
                f'Global.pretrained_model={weight_path.replace(".pdparams","")}'
            ])
        if save_dir is not None:
            config.update([f'Global.save_inference_dir={save_dir}'])
        config_path = self._config_path
        config.dump(config_path)

        self.runner.export(config_path, [], None)

    def infer(self, model_dir, input_path, device='gpu', save_dir=None):
        model_dir = abspath(model_dir)
        input_path = abspath(input_path)
        if save_dir is not None:
            save_dir = abspath(save_dir)
        else:
            # `save_dir` is None
            save_dir = abspath(os.path.join('output', 'infer'))
        config_path = os.path.join(self.runner.runner_root_path,
                                   'deploy/configs/inference_cls.yaml')
        config = self.config.copy()
        config.load(config_path)
        config.update([f'Global.inference_model_dir={model_dir}'])
        if input_path is not None:
            config.update([f'Global.infer_imgs={input_path}'])
        if device is not None:
            config.update([f'Global.use_gpu={device.split(":")[0]=="gpu"}'])

        config_path = self._config_path
        config.dump(config_path)
        self.runner.infer(config_path, [], device)

    def compression(self,
                    weight_path,
                    dataset=None,
                    batch_size=None,
                    learning_rate=None,
                    epochs_iters=None,
                    device='gpu',
                    use_vdl=True,
                    save_dir=None,
                    input_shape=None):
        weight_path = abspath(weight_path)
        if dataset is not None:
            dataset = abspath(dataset)
        if save_dir is not None:
            save_dir = abspath(save_dir)
        else:
            # `save_dir` is None
            save_dir = abspath(os.path.join('output', 'compress'))

        # Update YAML config file
        config = self.config.copy()
        config.update_dataset(dataset)
        config.update_device(device)

        if batch_size is not None:
            config.update_batch_size(batch_size)
        if learning_rate is not None:
            config.update_lr_scheduler(learning_rate)
        if epochs_iters is not None:
            config.update([f'Global.epochs={epochs_iters}'])
        if weight_path is not None:
            config.update([
                f'Global.pretrained_model={weight_path.replace(".pdparams","")}'
            ])
        if use_vdl:
            config.update([f'Global.use_visualdl={use_vdl}'])
        if save_dir is not None:
            config.update([f'Global.output_dir={save_dir}'])
        config_path = self._config_path
        config.dump(config_path)

        model_name = self.name
        if self.name == 'PPLCNetV2_base_ShiTu':
            model_name = 'RecModel'

        self.runner.compression(config_path, [], device, save_dir, model_name)