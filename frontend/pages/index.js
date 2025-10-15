import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import axiosInstance from "../utils/axiosInstance";
import { useUserStore } from "../store/userStore";
import "../styles/Home.css";

export default function Home() {
  const router = useRouter();
  const { user, setUser } = useUserStore(); 
  const [notes, setNotes] = useState([]);
  const [newNote, setNewNote] = useState({ note_title: "", note_content: "" });
  const [editingNote, setEditingNote] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  useEffect(() => {
    if (!user) {
      router.push("/signin");
    }
  }, [user, router]);

  const fetchNotes = async () => {
    if (!user) return;
    try {
      setLoading(true);
      const res = await axiosInstance.get(`/notes?user_id=${user.user_id}`);
      setNotes(res.data);
    } catch (err) {
      console.error("Error fetching notes:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, [user]);

  const showMessage = (msg, type) => {
    setMessage(msg);
    setMessageType(type);
    setTimeout(() => {
      setMessage("");
      setMessageType("");
    }, 3000);
  };

  const handleAdd = async () => {
    if (!newNote.note_title || !newNote.note_content) {
      showMessage("Please enter both title and content!", "error");
      return;
    }
    try {
      setLoading(true);
      await axiosInstance.post(`/notes?user_id=${user.user_id}`, newNote);
      setNewNote({ note_title: "", note_content: "" });
      fetchNotes();
      showMessage("Note added successfully!", "success");
    } catch (err) {
      console.error("Error adding note:", err);
      showMessage("Failed to add note!", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (note) => {
    setEditingNote(note);
    setNewNote({
      note_title: note.note_title,
      note_content: note.note_content,
    });
  };

  const handleUpdate = async () => {
    if (!editingNote) return;

    try {
      setLoading(true);
      await axiosInstance.put(`/notes/${editingNote.note_id}`, newNote);
      setEditingNote(null);
      setNewNote({ note_title: "", note_content: "" });
      fetchNotes();
      showMessage("Note updated successfully!", "success");
    } catch (err) {
      console.error("Error updating note:", err);
      showMessage("Failed to update note!", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (note_id) => {
    if (!confirm("Are you sure you want to delete this note?")) return;
    try {
      await axiosInstance.delete(`/notes/${note_id}`);
      fetchNotes();
      showMessage("Note deleted successfully!", "success");
    } catch (err) {
      console.error("Error deleting note:", err);
      showMessage("Failed to delete note!", "error");
    }
  };

  const handleLogout = () => {
    setUser(null);
    router.push("/signin");
  };

  if (!user) return null;

  return (
    <div className="notes-container">
      <div className="header">
        <h1>Your Available Notes</h1>
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </div>

      {/* Notification */}
      {message && <div className={`notification ${messageType}`}>{message}</div>}

      <div className="input-section">
        <input
          type="text"
          placeholder="Enter Note Title"
          value={newNote.note_title}
          onChange={(e) =>
            setNewNote({ ...newNote, note_title: e.target.value })
          }
        />

        <textarea
          placeholder="Write your note content..."
          value={newNote.note_content}
          onChange={(e) =>
            setNewNote({ ...newNote, note_content: e.target.value })
          }
        ></textarea>

        {editingNote ? (
          <button onClick={handleUpdate} disabled={loading}>
            {loading ? "Updating..." : "Update Note"}
          </button>
        ) : (
          <button onClick={handleAdd} disabled={loading}>
            {loading ? "Adding..." : "Add Note"}
          </button>
        )}
      </div>

      <div className="card-grid">
        {notes.length === 0 ? (
          <p className="no-notes">No notes yet!</p>
        ) : (
          notes.map((note) => (
            <div className="note-card" key={note.note_id}>
              <div className="note-content">
                <h2>{note.note_title}</h2>
                <p>{note.note_content}</p>
              </div>
              <div className="card-actions">
                <button className="edit-btn" onClick={() => handleEdit(note)}>
                  Edit
                </button>
                <button
                  className="delete-btn"
                  onClick={() => handleDelete(note.note_id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
