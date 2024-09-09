import numpy as np

class CameraParameters:
    """Classe para carregar e armazenar os parâmetros da câmera."""
    
    def __init__(self):
        self.camera_matrix, self.dist_coeffs = self.load_parameters()

    @staticmethod
    def load_parameters():
        """Carrega os parâmetros da câmera."""
        camera_matrix = np.array([
            [331.3076549, 0.0, 630.16629165],
            [0.0, 333.06212044, 458.44728206],
            [0.0, 0.0, 1.0]
        ])

        dist_coeffs = np.array([
            1.40813986e+01, 7.83197268e+00, -3.97740954e-04, -4.44407448e-05, 2.72931297e-01,
            1.42843953e+01, 1.27794122e+01, 1.65578909e+00, -7.07882378e-04, 9.66729468e-05,
            3.69522034e-05, 7.40627933e-05, 4.73807169e-03, 4.47503227e-03
        ])

        return camera_matrix, dist_coeffs
