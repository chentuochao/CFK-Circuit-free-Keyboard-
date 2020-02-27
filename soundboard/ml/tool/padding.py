from typing import List, Tuple

import torch
import torch.nn.functional as f


def pad_input(input_array: List[torch.Tensor]) -> Tuple[torch.Tensor, List[int], List[int]]:
    """
    Pad a input array
    :param input_array: List[N (batch size)] of torch.Tensor with t (trace count) x f (feature size) x l (length)
    """
    trace_counts = [single_input.shape[0] for single_input in input_array]
    input_lengths = [single_input.shape[2] for single_input in input_array]
    target_length = max(input_lengths)
    padded_input_array = [f.pad(single_input, [0, target_length - single_input.shape[2]])
                          for single_input in input_array]
    padded_array = torch.cat(padded_input_array, dim=0)
    return padded_array, trace_counts, input_lengths


def unpad_output(input_array: torch.Tensor, trace_counts: List[int], input_lengths: List[int]) -> List[torch.Tensor]:
    output_array = []
    current_pos = 0
    for trace_count, input_length in zip(trace_counts, input_lengths):
        next_pos = current_pos + trace_count
        output_array += [input_array[current_pos: next_pos, :, 0: input_length]]
        current_pos = next_pos
    return output_array
