# Copyright 2019 snactclass software
# Author: Emille E. O. Ishida
#         Based on initial prototype developed by the CRP #4 team
#
# created on 10 August 2019
#
# Licensed GNU General Public License v3.0;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__all__ = ['uncertainty_sampling', 'random_sampling']

import numpy as np
import pandas as pd

def uncertainty_sampling(class_prob: np.array, test_ids: np.array,
                         queryable_ids: np.array, batch=1,
                         screen=False) -> list:
    """Search for the sample with highest uncertainty in predicted class.

    Parameters
    ----------
    class_prob: np.array
        Classification probability. One value per class per object.
    test_ids: np.array
        Set of ids for objects in the test sample.
    queryable_ids: np.array
        Set of ids for objects available for querying.
    batch: int (optional)
        Number of objects to be chosen in each batch query.
        Default is 1.
    dump: bool (optional)
        If True display on screen the shift in index and
        the difference in estimated probabilities of being Ia
        caused by constraints on the sample available for querying.

    Returns
    -------
    query_indx: list
            List of indexes identifying the objects from the test sample
            to be queried in decreasing order of importance.
    """

    # calculate distance to the decision boundary - only binary classification
    dist = abs(class_prob[:, 1] - 0.5)

    # get indexes in increasing order
    order = dist.argsort()
                           
    # only allow objects in the query sample to be chosen
    flag = list(pd.Series(data=test_ids[order]).isin(queryable_ids))
    
    # arrange queryable elements in increasing order
    flag = np.array(flag)
    final_order = order[flag]

    if screen:
        print('\n Inside UncSampling: ')
        print('       query_ids: ', test_ids[final_order][:batch], '\n')
        print('   number of test_ids: ', test_ids.shape[0])
        print('   number of queryable_ids: ', len(queryable_ids), '\n')
        print('   *** Displacement caused by constraints on query****')
        print('   0 -> ', list(order).index(final_order[0]))
        print('   ', class_prob[order[0]], '-- > ', class_prob[final_order[0]], '\n')

    # return the index of the highest uncertain objects which are queryable
    return list(final_order)[:batch]


def random_sampling(test_ids: np.array, queryable_ids: np.array,
                    batch=1, seed=42, screen=False) -> list:
    """Randomly choose an object from the test sample.

    Parameters
    ----------
    test_ids: np.array
        Set of ids for objects in the test sample.
    queryable_ids: np.array
        Set of ids for objects available for querying.
    batch: int (optional)
        Number of objects to be chosen in each batch query.
        Default is 1.
    screen: bool (optional)
        If True display on screen the ids of queried objects.
        Default is False.
    seed: int (optional)
        Seed for random number generator. Default is 42.

    Returns
    -------
    query_indx: list
            List of indexes identifying the objects from the test sample
            to be queried.
    """

    # randomly select indexes to be queried
    np.random.seed(seed)
    indx = np.random.randint(low=0, high=len(test_ids), size=len(test_ids))

    # only allow objects in the query sample to be chosen
    flag = list(pd.Series(data=test_ids[order]).isin(queryable_ids))

    flag = np.array(flag)

    if screen:
        print('\n Inside RandomSampling: ')
        print('       query_ids: ', test_ids[indx[flag]][:batch], '\n')
        print('   number of test_ids: ', test_ids.shape[0])
        print('   number of queryable_ids: ', len(queryable_ids), '\n')   

    # return the corresponding batch size
    return list(indx[flag])[:batch]


def main():
    return None


if __name__ == '__main__':
    main()
