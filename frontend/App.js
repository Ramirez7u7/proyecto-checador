import React, { useState, useRef, useEffect } from 'react';
import { View, Text, TouchableOpacity, FlatList, Modal, StyleSheet, ActivityIndicator } from 'react-native';
import api from './src/services/api';

export default function HomeScreen() {
  const [historial, setHistorial] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fotoCapturada, setFotoCapturada] = useState(null);
  const videoRef = useRef(null);

  // Inicializa la Cámara
  useEffect(() => {
    iniciarCamara();
  }, []);

  const iniciarCamara = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error("Error al acceder a la cámara:", err);
    }
  };

  // Captura la foto y la envía a la API
  const marcarAsistencia = async () => {
    if (!videoRef.current) return;

    setLoading(true);
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth || 640;
    canvas.height = videoRef.current.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) {
        setLoading(false);
        alert("Error al tomar la captura de la cámara.");
        return;
      }

      setFotoCapturada(URL.createObjectURL(blob));

      const formData = new FormData();
      formData.append('file', blob, 'captura.jpg');

      try {
        const response = await api.post('/api/v1/checador/marcar', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        setLoading(false);
        alert(response.data.mensaje || 'Asistencia registrada con éxito');
      } catch (error) {
        setLoading(false);
        const mensajeError = error.response?.data?.detail || 'Error al procesar la asistencia';
        alert(mensajeError);
      }
    }, 'image/jpeg');
  };






  const cargarHistorial = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/v1/checador/historial');
      setHistorial(response.data.asistencias);
      setLoading(false);
      setModalVisible(true);
    } catch (error) {
      setLoading(false);
      alert('Error al consultar el historial de asistencias.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.tituloApp}> Checador Facial oc V4 Marksucaritas Facebook </Text>

      {/* Contenedor de cámara maximizado */}
      <View style={styles.camaraContainer}>
        <video
          ref={videoRef}
          autoPlay
          playsInline
          style={{ width: '100%', height: '100%', borderRadius: 12, objectFit: 'cover' }}
        />
      </View>

      {loading && <ActivityIndicator size="large" color="#007bff" style={{ marginVertical: 10 }} />}

      {/* Botones más grandes con TouchableOpacity */}
      <View style={styles.actionArea}>
        <TouchableOpacity style={[styles.btnGrande, styles.btnMarcar]} onPress={marcarAsistencia}>
          <Text style={styles.btnTexto}> Identificate Prro Hijo P...</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.btnGrande, styles.btnHistorial]} onPress={cargarHistorial}>
          <Text style={styles.btnTexto}> Registros</Text>
        </TouchableOpacity>
      </View>

      {/* Modal para desplegar el historial */}
      <Modal visible={modalVisible} animationType="slide" transparent={false}>
        <View style={styles.modalContent}>
          <Text style={styles.tituloModal}> Historial de Entradas</Text>

          <FlatList
            data={historial}
            keyExtractor={(item, index) => index.toString()}
            contentContainerStyle={{ paddingBottom: 20 }}
            renderItem={({ item }) => (
              <View style={styles.itemCardCompact}>
                <View style={styles.cardHeader}>
                  <Text style={styles.nombreUserCompact}> {item.name}</Text>
                  <Text style={styles.badgeHora}>{item.hora}</Text>
                </View>
                <Text style={styles.textoDetalleCompact}> Fecha: {item.fecha}</Text>
              </View>
            )}
            ListEmptyComponent={<Text style={styles.emptyText}>No hay asistencias registradas hoy.</Text>}
          />

          <TouchableOpacity style={styles.btnCerrarModal} onPress={() => setModalVisible(false)}>
            <Text style={styles.btnTexto}>Cerrar</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 15,
    paddingVertical: 20,
    backgroundColor: '#0f0f11', 
  },
  tituloApp: {
    fontSize: 24,
    fontWeight: 'bold',
    marginVertical: 10,
    color: '#ffffff',
  },
  camaraContainer: {
    width: '100%',
    flex: 1,
    maxHeight: '65%',
    backgroundColor: '#1a1a1e',
    borderRadius: 16,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#2a2a30',
  },
  actionArea: {
    width: '100%',
    paddingVertical: 10,
    gap: 12,
  },
  btnGrande: {
    width: '100%',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  btnMarcar: {
    backgroundColor: '#007bff',
  },
  btnHistorial: {
    backgroundColor: '#28a745',
  },
  btnTexto: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
    letterSpacing: 0.5,
  },
  modalContent: {
    flex: 1,
    padding: 20,
    paddingTop: 40,
    backgroundColor: '#121214', // Fondo oscuro para el modal
  },
  tituloModal: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    textAlign: 'center',
    color: '#ffffff',
  },
  // Estilo compacto para cada card
  itemCardCompact: {
    backgroundColor: '#1e1e24',
    padding: 10,
    borderRadius: 8,
    marginBottom: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#007bff',
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  nombreUserCompact: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  badgeHora: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#28a745',
    backgroundColor: '#142918',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
  },
  textoDetalleCompact: {
    fontSize: 12,
    color: '#a0a0ab',
  },
  emptyText: {
    textAlign: 'center',
    marginTop: 20,
    color: '#71717a',
  },
  btnCerrarModal: {
    backgroundColor: '#dc3545',
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
});