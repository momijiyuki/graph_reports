import matplotlib.pyplot as plt
import numpy as np
import os

from pygsp import graphs

from gsp_python.src import util


def plot_gft_spectrum(L, graph_signal, title, save_path):
    # グラフラプラシアン行列の固有値と固有ベクトルを計算
    eigenvalues, eigenvectors = np.linalg.eigh(L)

    eigenvectors = eigenvectors[:, np.argsort(eigenvalues)]
    eigenvalues.sort()

    # グラフ信号とフーリエ基底の内積を計算
    print(eigenvectors.T.shape, graph_signal.shape)
    gft_coefficients = eigenvectors.T @ graph_signal

    # 結果をプロット
    plt.figure(figsize=(8, 6))
    # plt.stem(eigenvalues, np.abs(gft_coefficients))
    plt.stem(eigenvalues, gft_coefficients)
    plt.xlabel('Graph Frequencies (Eigenvalues)')
    plt.ylabel('GFT Coefficients')
    plt.title(f'GFT Spectrum({title})')
    plt.grid(True)

    # プロットを画像ファイルとして保存
    plt.savefig(os.path.join(save_path, f'gft_spectrum_{title}.png'))
    plt.close()


def plot_graphs(L, G, pos, region):
    eigenvalues, eigenvectors = np.linalg.eigh(L)

    eigenvectors = eigenvectors[:, np.argsort(eigenvalues)]
    eigenvalues.sort()

    for idx in range(5):
        eigenvector = eigenvectors[:, idx]
        # 固有ベクトルを正規化
        # 値が小さいと点が表示されないので1を足す
        eigenvector = (eigenvector - np.min(eigenvector)) / (np.max(eigenvector) - np.min(eigenvector)) + 1

        # 固有ベクトルを頂点領域のグラフ信号としてプロット
        util.draw_graph(
            G, pos, eigenvector,
            image=f"u{idx +1}({region}).png",
            fig_title=f"u{idx +1}({region})"
        )

# /workspaces/py_git/graph/gsp_python/train/Australia_Perth.npz

def main():
    region = "Australia_Perth"
    npz_path = util.top_dir() / "train" / f"{region}.npz"
    npz = np.load(npz_path)
    N, T, W, L, data, pos = (
        npz["N"],
        npz["T"],
        npz["W"],
        npz["L"],
        npz["data"],
        npz["pos"],
    )

    G = graphs.Graph(W)

    print(L.shape)

    t = 0
    ### Normalize data
    normilized_data = util.normalize_graph_signal(data[:, t])

    ### Plot signal
    util.draw_graph(
        G,
        pos,
        data[:, t],
        image=f"normalized_signal({region}, t=0).png",
        use_node_values=normilized_data,
        fig_title=f"normalized_signal({region},t=0)",
    )
    plot_graphs(L, G, pos, region)

    plot_gft_spectrum(L, normilized_data, region, './')





if __name__=="__main__":
    main()
